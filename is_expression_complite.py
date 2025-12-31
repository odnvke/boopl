from util import is_pointer, get_number
from tokens import _and, _end, _false, _goto, _if, _not, _or, _print, _true, _xor, _next_str, _space

def is_expression_complite(tokens: list) -> (bool, int):
    try:
        len_tokens = len(tokens)

        if len_tokens > 4:
            raise Exception(f"не удалось обработать последовательность токенов {tokens} (больше 4)")

        if len_tokens == 1:
            #   P10
            if is_pointer(string=tokens[0]):
                return [111, get_number(tokens[0])]

            #   E
            if tokens[0] == _end:
                return [112]
        
            return False
        
        if len_tokens == 2:
            _0 = tokens[0]; _1 = tokens[1]
            
            if _0.isdigit():
                #   10 F
                if _1 == _false:
                    return [100, int(_0)]
                
                #   10 T
                if _1 == _true:
                    return [101, int(_0)]
                
                if _1.isdigit():
                    return[113, int(_0), int(_1)]
                return False
            
            #   G P10
            if _0 == _goto and is_pointer(_1):
                return [102, int(get_number(_1))]
            
            #   I 10
            if _0 == _if and _1.isdigit():
                return [103, int(_1)]

            #   P T | P F | P 10
            if _0 == _print:
                if _1 == _true:
                    return [104]
                if _1 == _false:
                    return [105]
                if _1.isdigit():
                    return [106, int(_1)]
                if _1 == _next_str:
                    return [114]
                if _1 == _space:
                    return [115]
                
            
            return False
        
        if len_tokens == 3:
            _0 = tokens[0]; _1 = tokens[1]; _2 = tokens[2]

            # 10 N 10
            if _0.isdigit() and _1 == _not and _2.isdigit():
                return [107, int(_0), int(_2)]
            
        if len_tokens == 4:
            _0 = tokens[0]; _1 = tokens[1]; _2 = tokens[2]; _3 = tokens[3]
            
            if _0.isdigit() and _2.isdigit() and _3.isdigit():
                if _1 == _or:
                    return [108, int(_0), int(_2), int(_3)]
                if _1 == _and:
                    return [109, int(_0), int(_2), int(_3)]
                if _1 == _xor:
                    return [110, int(_0), int(_2), int(_3)]
                
            return False

        return False
    except Exception as e:
        raise Exception(f"Ошибка обработки токенов {tokens}: {e}")