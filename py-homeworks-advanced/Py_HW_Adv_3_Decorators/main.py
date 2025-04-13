import os
from datetime import datetime
from functools import wraps

# 1 часть домашнего задания
def logger1(old_function):
    def write_log(result, *args, **kwargs):
        path = 'main.log'
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} - Вызвана функция {old_function}'
                    f' с аргументами {args, kwargs}. Возвращаемое значение: {result}\n')
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        write_log(result, *args, **kwargs)
        return result

    return new_function

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger1
    def hello_world():
        return 'Hello World'

    @logger1
    def summator(a, b=0):
        return a + b

    @logger1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

# 2 часть домашнего задания
def logger2(path):
    def write_log(name_function, result, *args, **kwargs):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} - Вызвана функция {name_function}'
                    f' с аргументами {args, kwargs}. Возвращаемое значение: {result}\n')

    def __logger2(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            write_log(old_function, result, *args, **kwargs)
            return result

        return new_function

    return __logger2

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

# 3 часть домашнего задания
def test_3():
    path = 're_csv.log'
    path_csv = 'phonebook.csv'
    if os.path.exists(path):
        os.remove(path)

    @logger2(path)
    def re_csv():
        os.system("python ./Py_HW_Adv_5_Regexp/main.py")
        return 'Attempts convert phonebook_raw.csv'

    assert 'Attempts convert phonebook_raw.csv' == re_csv(), "Функция возвращает 'Attempts convert phonebook_raw.csv'"

    assert os.path.exists(path), f'файл {path} должен существовать'

    assert os.path.exists(path_csv), f'файл {path_csv} должен существовать'

    with open(path) as log_file:
         log_file_content = log_file.read()

    assert 're_csv' in log_file_content, 'должно записаться имя функции'

if __name__ == '__main__':

    test_1()
    test_2()
    test_3()