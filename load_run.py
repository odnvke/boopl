import sys
import os

def load_program(filename):
    """Загружает программу без комментариев"""
    program = []
    
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден")
        return None
    
    with open(filename, 'r') as f:
        line_num = 0
        for line in f:
            line_num += 1
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            try:
                # Разбиваем строку на части
                parts = line.split()
                if not parts:
                    continue
                
                # Берем максимум 4 числа
                instr = []
                for i in range(min(4, len(parts))):
                    try:
                        # Преобразуем в число
                        num = int(float(parts[i]))  # Обрабатываем и int и float
                        instr.append(num)
                    except ValueError:
                        # Если не число, ставим 0
                        instr.append(0)
                        print(f"Внимание: строка {line_num} - '{parts[i]}' не является числом")
                
                # Дополняем до 4 элементов
                while len(instr) < 4:
                    instr.append(0)
                
                program.append(instr)
                
            except Exception as e:
                print(f"Ошибка в строке {line_num}: {e}")
                continue
    
    if program:
        print(f"Загружено {len(program)} инструкций")
        return program
    else:
        print("Не удалось загрузить программу")
        return None