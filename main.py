import sys
import os
import hashlib
import numpy as np
from util import is_valid
from preprocces import preprocces, get_matrix, clear_matrix, flush_tokens

def get_file_hash(filename):
    try:
        with open(filename, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def show_error_context(filename, error_line=None, context_lines=3):
    """Показывает контекст ошибки из исходного файла"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        if error_line is not None:
            start = max(0, error_line - context_lines)
            end = min(len(lines), error_line + context_lines + 1)
            
            print("\nКонтекст ошибки в исходном файле:")
            print("-" * 50)
            for i in range(start, end):
                prefix = ">>> " if i + 1 == error_line else "    "
                print(f"{prefix}Строка {i+1}: {lines[i].rstrip()}")
            print("-" * 50)
        else:
            # Показываем последние строки файла
            print("\nПоследние строки исходного файла:")
            print("-" * 50)
            start = max(0, len(lines) - context_lines * 2)
            for i in range(start, len(lines)):
                print(f"    Строка {i+1}: {lines[i].rstrip()}")
            print("-" * 50)
    except Exception as e:
        print(f"Не удалось прочитать исходный файл для контекста: {e}")

def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py <файл>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден")
        sys.exit(1)
    
    base_name = os.path.splitext(filename)[0]
    compiled_file = f"{base_name}_compiled.txt"
    hash_file = f"{base_name}_compiled.hash"
    
    current_hash = get_file_hash(filename)
    need_compile = True
    
    if os.path.exists(hash_file) and os.path.exists(compiled_file):
        with open(hash_file, 'r') as f:
            saved_hash = f.read().strip()
        
        if current_hash == saved_hash:
            #print("Код не изменился, используем существующий")
            need_compile = False
            return 0
    
    if need_compile:
        print(f"Компиляция {filename}...")
        clear_matrix()

        line_num = 0
        last_tokens = []
        
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Читаем построчно для лучшего отслеживания ошибок
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    tokens_in_line = line.strip().split()
                    last_tokens.extend(tokens_in_line)
                    
                    for token in tokens_in_line:
                        if is_valid(token):
                            preprocces(token)
                        else:
                            raise Exception(f"Неизвестный токен '{token}' в строке {line_num}")
                flush_tokens()
            matrix = get_matrix()
                
            with open(compiled_file, 'w') as f:
                for row in matrix:
                    row_int = [int(x) for x in row]
                    f.write(f"{row_int[0]} {row_int[1]} {row_int[2]} {row_int[3]}\n")
                    
            if current_hash:
                with open(hash_file, 'w') as f:
                    f.write(current_hash)
            
            print(f"✓ Компиляция успешна. Создано {len(matrix)} инструкций.")
            return 0
                
        except Exception as e:
            print(f"\n✗ Ошибка компиляции в строке {line_num}: {e}")
            
            # Сохраняем последние токены для отладки
            if last_tokens:
                print(f"Последние обработанные токены: {last_tokens[-10:]}")
            
            # Показываем контекст ошибки
            show_error_context(filename, line_num)
            
            # Удаляем скомпилированный файл, если он был создан с ошибками
            if os.path.exists(compiled_file):
                os.remove(compiled_file)
            
            # Показываем текущее состояние матрицы (для отладки)
            try:
                matrix = get_matrix()
                if len(matrix) > 0:
                    print(f"\nУспешно скомпилировано инструкций: {len(matrix)}")
                    print("Последние скомпилированные инструкции:")
                    for i, row in enumerate(matrix[-5:] if len(matrix) >= 5 else matrix):
                        print(f"  Инструкция {len(matrix)-len(matrix[-5:])+i+1}: {row}")
            except:
                pass
                
            return 1

if __name__ == "__main__":
    sys.exit(main())