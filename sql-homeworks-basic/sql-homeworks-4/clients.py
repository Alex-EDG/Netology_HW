import sys
from  PGSQL import PgSQL
import logging

class ClientsDB:
    def __init__(self):
        self.db = PgSQL()

        logging.basicConfig(
            level=logging.INFO,
            filename='logs.log',
            filemode='a',
            format='[%(asctime)s] %(levelname)s - %(message)s'
        )

    def input_client_data(self):
        print("\033[H\033[J", end="")
        email = input('Введите Email клиента:')
        name = input('Введите имя клиента:')
        surname = input('Введите фамилию клиента:')
        phone_number = input('Введите № телефона клиента(\033[94mEnter\033[0m - пропустить):')
        data={'email':email, 'name': name, 'surname': surname, 'phone_number': phone_number}
        return data

    def create(self):
        self.db.create()
        logging.info('Созданы таблицы БД')

    def insert(self, email, name, surname, phone_number=''):
        self.db.insert(email, name, surname, phone_number)
        logging.info(f'В БД добавлены данные: email={email}, name={name}, surname={surname}, phone_number={phone_number}')

    def update(self, email, name, surname, phone_number=''):
        print("\033[H\033[J", end="")
        client_id = input('Введите \033[94mid\033[0m клиента данные которого необходимо обновить:')
        self.db.update(client_id, email, name, surname, phone_number)
        logging.info(f'В БД обновлены данные: email={email}, name={name}, surname={surname}, phone_number={phone_number}')

    def delete(self):
        print("\033[H\033[J", end="")
        client_id = input('Введите \033[94mid\033[0m клиента данные которого необходимо удалить:')
        self.db.delete(client_id)
        logging.info(f'Для клиента с id={client_id} в БД удалены данные')

    def upd_phone_number(self):
        print("\033[H\033[J", end="")
        client_id = input('Введите \033[94mid\033[0m клиента № телефона которого необходимо изменить:')
        phone_number = input('Введите № телефона клиента:')
        mode = input('Введите \033[94mdel\033[0m для удаления № телефона или \033[94madd\033[0m для добавления:')
        self.db.upd_phone_number(client_id, phone_number, mode)
        logging.info(f'Для клиента с id={client_id} в БД удалены/добавлены данные о № телефона')

    def select(self):
        print("\033[H\033[J", end="")
        email = input('Введите Email клиента(\033[94mEnter\033[0m - пропустить):')
        name = input('Введите имя клиента(\033[94mEnter\033[0m - пропустить):')
        surname = input('Введите фамилию клиента(\033[94mEnter\033[0m - пропустить):')
        phone_number = input('Введите № телефона клиента(\033[94mEnter\033[0m - пропустить):')
        search_request = [email, name, surname, phone_number]
        for idx, item in enumerate(search_request):
            if item == '':
                search_request[idx]=None
        result = self.db.select(search_request)
        logging.info(f'Выборка данных из БД если: email={email}, name={name}, surname={surname}, phone_number={phone_number}')
        for client in result:
            print(f'client_id={client['id']}, email={client['email']}, name={client['name']}, surname={client['surname']}, phone_number={client['phone_number']}')

def ui():
    print("\033[H\033[J", end="")
    while True:
        ui_text = ('Выбрать действие:\n\n'
                   '\033[94m1\033[0m - Создать новую БД(таблицы\n'
                   '\033[94m2\033[0m - Добавить клиента\n'
                   '\033[94m3\033[0m - Обновить данные клиента\n'
                   '\033[94m4\033[0m - Удалить клиента\n'
                   '\033[94m5\033[0m - Добавить/Удалить телефонный № клиента\n'
                   '\033[94m6\033[0m - Поиск записей клиента(ов) по данным\n'
                   '\033[94m7,8,9,0\033[0m - Выход\n'
                   '?')
        try:
            ui_choice = int(input(ui_text)[0])
            if ui_choice == 0 or ui_choice > 6:
                sys.exit()
        except ValueError:
            print('Неверный ввод, должна быть цифра')
            continue
        else:
            return ui_choice

if __name__ == '__main__':

    db_pgsql = ClientsDB()
    choice = ui()

    if choice == 1:
        db_pgsql.create()
    elif choice == 2:
        db_pgsql.insert(**db_pgsql.input_client_data())
    elif choice == 3:
        db_pgsql.update(**db_pgsql.input_client_data())
    elif choice == 4:
        db_pgsql.delete()
    elif choice == 5:
        db_pgsql.upd_phone_number()
    elif choice == 6:
        db_pgsql.select()