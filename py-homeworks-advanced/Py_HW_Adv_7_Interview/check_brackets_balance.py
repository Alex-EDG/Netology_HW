from stack import Stack


def is_brackets_balance(string: str) -> tuple[bool, int]:
    """
    :param string: String for analysis brackets balance
    :return: (True if brackets balance exist else False , Number of founded brackets)
    """
    stack: Stack = Stack() # создаем пустой стек
    result: bool = False
    founded_brackets: int = 0
    for chapter in string:
        if chapter in '([{': # ищем открывающую скобку
            founded_brackets += 1
            stack.push(chapter) # добавляем её в стек
        elif chapter in ')]}': # ищем закрывающую скобку
            founded_brackets += 1
            if not stack: # если стек пуст, значит скобки не сбалансированы
                break
            last = stack.pop() # извлекаем последнюю скобку из стека
            if ((chapter == ')' and last == '(')
                or (chapter == '}' and last == '{')
                or (chapter == ']' and last == '[')):
                result = True
            else:
                result = False
                break
    return result, founded_brackets

if __name__ == '__main__':

    s : str = input('Введите анализируемую строку:') # считываем анализируемую строку
    if is_brackets_balance(s)[0]:
        print("Сбалансировано")
    elif not is_brackets_balance(s)[0] and is_brackets_balance(s)[1] == 0:
        print("Нет скобок, нет нарушения их баланса ;-)")
    else:
        print("Не сбалансировано")