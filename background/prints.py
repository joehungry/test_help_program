def err(string: str):
    print(f'\033[91m{string}\033[0m')

def ask(*string: str) -> str:
    for i in string:
        print(i)
    askvar = input('>> ')
    return askvar