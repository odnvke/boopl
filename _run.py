import numpy as np
import sys
import os

from load_run import load_program

def load_pointers(program, memory_pointer, size) -> np.ndarray:
    count = 0
    for i in range(size):
        if program[i, 0] == 111:
            memory_pointer[program[i, 1]] = i
            #print("load pointer:", i)
            count += 1
    return memory_pointer

def execute_program(program):
    """Исполняет программу"""
    
    point = 0
    memory_pointer = np.zeros(10000, dtype="uint32")
    memory = np.zeros(10000, dtype="uint8")
    program = np.array(program)
    print("Начало исполнения:")
    size, _ = program.shape
    memory_pointer = load_pointers(program, memory_pointer, size)
    #print(program, "\n\n")
    while True:
        line = program[point]
        #print(line, end="")
        opcode = line[0]
        if opcode == 100:  # 10 F;  100 -0 
            memory[line[1]] = 0
            #print(f"M[{line[1]}] = false")
                
        elif opcode == 101:  # 10 T;  100 -0
            memory[line[1]] = 1
            #print(f"M[{line[1]}] = true")
                
        elif opcode == 102:  # G P10  102 -1      
            point = memory_pointer[line[1]]
            #print(f"GOTO {point}")  
            
            
        elif opcode == 103:  # I 10
            if memory[line[1]] == 0:
                #print(f"IF M[{line[1]}]==false -> пропуск")
                point += 1
                
        elif opcode == 104:  # P T
            print("#", end="")
            
                
        elif opcode == 105:  # P F
            print(".", end="")
         
        elif opcode == 106:  # P 10
            if memory[line[1]]: print("#", end="") 
            else: print(".", end="")

                
        elif opcode == 107:  # 10 N 10
            memory[line[1]] = not memory[line[2]]
            #print(f"M[{line[1]}] = NOT M[{line[2]}]")
                
        elif opcode == 108:  # 10 O 10 10
            memory[line[1]] = 1 if (memory[line[2]] == 1 or memory[line[3]] == 1) else 0
            #print(f"M[{line[0]}] = M[{a}] OR M[{b}]")
                
        elif opcode == 109:  # 10 A 10 10
            memory[line[1]] = 1 if (memory[line[2]] == 1 and memory[line[3]] == 1) else 0
            #print(f"M[{line[0]}] = M[{a}] AND M[{b}]")
                            
        elif opcode == 110:  # 10 X 10 10
            memory[line[1]] = 1 if (memory[line[2]] == 1) != (memory[line[3]] == 1) else 0
            #print(f"M[{line[1]}] = M[{line[2]}] XOR M[{line[3]}]")
                
        elif opcode == 111:  # P10
            #print("2",end="")
            pass
                
        elif opcode == 112:  # E
            print(f"конец программы через E")
            break
        
        elif opcode == 113: # 10 10
            memory[line[1]] = memory[line[2]]
        

        if opcode == 114:
            print()
        
        if opcode == 115:
            print(" ", end="")
        
        point += 1
        
        if point >= size:
            break
            print(f"Конец программы")

def main():
    if len(sys.argv) < 2:
        print("Использование: python _run.py <скомпилированный_файл>")
        print("Пример: python run.py _ex_compiled.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    program = load_program(filename)
    
    if program:
        execute_program(program)

if __name__ == "__main__":
    main()