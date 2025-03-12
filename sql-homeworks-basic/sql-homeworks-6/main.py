import sys
from  SQL_Processor import SqlProcessor
import logging

class PubliherSales:
    def __init__(self):
        self.db = SqlProcessor()

        logging.basicConfig(
            level=logging.INFO,
            filename='logs.log',
            filemode='a',
            format='[%(asctime)s] %(levelname)s - %(message)s'
        )

    def create_db(self):
        self.db.create_tables()

    def input_db_data(self):
        self.db.fill_test_data()

    def db_query(self):
        print("\033[H\033[J", end="")
        publisher = input('Введите имя издателя:')
        result = self.db.querys(publisher)
        for record in result:
            print(f'{record[0]:<40} | {record[1]:<10} | {record[2]:<10} | {record[3]}')

def ui():
    print("\033[H\033[J", end="")
    while True:
        ui_text = ('Выбрать действие:\n\n'
                   '\033[94m1\033[0m - Создать новую БД(таблицы)\n'
                   '\033[94m2\033[0m - Создать новую БД из файла tests_data.json\n'
                   '\033[94m3\033[0m - Найти информацию о покупках книг определённого издателя\n'
                   '\033[94m4,5,6,7,8,9,0\033[0m - Выход\n'
                   '?')
        try:
            ui_choice = int(input(ui_text)[0])
            if ui_choice == 0 or ui_choice > 3:
                sys.exit()
        except ValueError:
            print('Неверный ввод, должна быть цифра')
            continue
        else:
            return ui_choice

if __name__ == '__main__':

    db_ps = PubliherSales()
    choice = ui()

    if choice == 1:
        db_ps.create_db()
    elif choice == 2:
        db_ps.input_db_data()
    elif choice == 3:
        db_ps.db_query()