import sys
import os
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Использование: python run.py <файл>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    if not os.path.exists(source_file):
        print(f"Файл '{source_file}' не найден")
        sys.exit(1)
    
    base_name = os.path.splitext(source_file)[0]
    compiled_file = f"{base_name}_compiled.txt"
    
    # Запускаем компиляцию и получаем статус
    compile_result = subprocess.run([sys.executable, "main.py", source_file])
    
    if compile_result.returncode != 0:
        print("✗ Компиляция завершилась с ошибкой. Программа не будет исполнена.")
        sys.exit(1)
    
    # Проверяем, создан ли скомпилированный файл
    if not os.path.exists(compiled_file):
        print("✗ Скомпилированный файл не создан!")
        sys.exit(1)
    
    # Проверяем размер файла
    size = os.path.getsize(compiled_file)
    if size == 0:
        print("✗ Скомпилированный файл пуст!")
        sys.exit(1)
    
    # Запускаем исполнение
    exec_result = subprocess.run([sys.executable, "_run.py", compiled_file])
    
    return exec_result.returncode

if __name__ == "__main__":
    sys.exit(main())