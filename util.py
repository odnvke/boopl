valid_tokens = ["F", "T", "A", "O", "N", "E", "G", "I", "X", "P", "S"]

def is_valid(_str) -> bool:
    if _str in valid_tokens:
        return True

    if _str.isdigit():
        return True
    
    return is_pointer(_str)

def is_pointer(string) -> bool:
    if type(string) is str and len(string) > 1:
        if string[0] == "P":
            for i in string[1: ]:
                if not i.isdigit():
                    return False
    
            return True
    
    return False

def get_number(string) -> bool:
    if type(string) is str and len(string) > 1:
        if string[0] == "P":
            return int(string[1: ])