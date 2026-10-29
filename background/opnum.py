def cap(num: int, cap: int) -> int:
    capped_num = num - (((cap) * int(num / cap)))
    return capped_num

def is_int(number: str) -> bool:
    try:
        int(number)
        return True
    except:
        return False

def is_num(number: str) -> bool:
    if is_int(number) == True:
        return True
    try:
        float(number)
        return True
    except:
        return False
    

def data_type(number: str) -> str:
    if number == 'True' or number == 'False':
        return 'Boolean'
    if is_num(number) == False:
        return 'notNum'
    if not '.' in str(number):
        return 'int'
    decimal_split = number.split('.')
    if len(decimal_split) != 2:
        pass
    elif int(decimal_split[1]) == 0:
        return 'int'
    return 'float'

if __name__ == '__main__':
    print(cap(6, 3))
    print(data_type('0.01'))
    print(data_type('6'))