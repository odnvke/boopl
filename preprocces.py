import numpy as np

matr = np.zeros((0, 4), dtype="uint32")

from is_expression_complite import is_expression_complite

tokens = []

def flush_tokens():
    """Принудительная обработка оставшихся токенов в конце файла"""
    global tokens, matr
    
    if tokens:
        # Проверяем, можно ли составить выражение из оставшихся токенов
        _list = is_expression_complite(tokens)
        
        if _list == False:
            raise Exception(f"Неполное выражение в конце файла: {tokens}")
        else:
            # Если можно, добавляем в матрицу
            matr2 = np.zeros((1, 4), dtype="uint32")
            for i in range(len(_list)):
                matr2[0, i] = int(_list[i])
            
            matr = np.vstack((matr, matr2))
            tokens = []  # Очищаем токены после обработки

def preprocces(string: str):
    global tokens, matr
    tokens.append(string)

    _list = is_expression_complite(tokens)

    if _list == False:
        return
    
    tokens = []
    matr2 = np.zeros((1, 4), dtype="uint32")
    for i in range(len(_list)):
        matr2[0, i] = int(_list[i])

    
    print(matr2)
    matr = np.vstack((matr, matr2))
        
def get_matrix() -> np.ndarray: 
    global matr
    return matr

def clear_matrix():
    """Очищает матрицу"""
    global matr, tokens
    matr = np.zeros((0, 4), dtype="uint32")
    tokens = []