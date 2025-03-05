import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import psycopg2.extras
from Common import Config
import logging

class PgSQL:
    def __init__(self):
        config = Config('settings.ini')
        self.db_params = {'user': config.read_config()['PostgreSQL']['user'],
                      'password': config.read_config()['PostgreSQL']['password'],
                          'host': config.read_config()['PostgreSQL']['host'],
                          'port': config.read_config()['PostgreSQL']['port'],
                        'dbname': config.read_config()['PostgreSQL']['db_name'],
                       'options': f'-c client_encoding={config.read_config()['PostgreSQL']['encoding']}'}
        logging.basicConfig(
            level=logging.INFO,
            filename='logs.log',
            filemode='a',
            format='[%(asctime)s] %(levelname)s - %(message)s'
        )
    # Создание структуры БД (таблиц)
    def create(self):

        tables_list = [
            """CREATE TABLE IF NOT EXISTS Emails (
               id SERIAL PRIMARY KEY,
               email VARCHAR(64) NOT NULL UNIQUE CHECK(Email !='')	
            );""",
            """CREATE TABLE IF NOT EXISTS Clients (
            id SERIAL PRIMARY KEY,
            email_id INTEGER NOT NULL REFERENCES Emails (id) ON DELETE CASCADE,
            name VARCHAR(32) NOT NULL,
            surname VARCHAR(96) NOT NULL	
            );""",
            """CREATE TABLE IF NOT EXISTS Phones (
               id SERIAL PRIMARY KEY,
               client_id INTEGER NOT NULL REFERENCES Clients (id) ON DELETE CASCADE,
               phone_number VARCHAR(18)	NOT NULL
            );""", ]

        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cur:
                    conn.autocommit = True
                    for sql in tables_list:
                        cur.execute(sql)
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на создание новой БД, соединение с PostgreSQL закрыто')

    # Добавить нового клиента
    def insert(self, email='', name='', surname='', phone_number=''):

        ins_email = """INSERT INTO Emails (email) VALUES (%s) RETURNING id"""
        ins_name_surname = """INSERT INTO Clients (email_id, name, surname) VALUES (%s, %s, %s) RETURNING id"""
        ins_phone_number = """INSERT INTO Phones (client_id, phone_number) VALUES (%s, %s)"""

        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cur:
                    conn.autocommit = True
                    if email != '' and name != '' and surname != '':
                        cur.execute(ins_email, [email])
                        email_id = cur.fetchone()[0]
                        cur.execute(ins_name_surname, [email_id, name, surname])
                        client_id = cur.fetchone()[0]
                        cur.execute(ins_phone_number, [client_id, phone_number])
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на внесение данных, соединение с PostgreSQL закрыто')

    # Изменить данные клиента
    def update(self, client_id, email='', name='', surname='', phone_number=''):

        upd_email = """UPDATE Emails SET email = %s WHERE id = %s"""
        upd_name_surname = """UPDATE Clients SET name = %s, surname = %s WHERE id = %s"""
        upd_phone_number = """UPDATE Phones SET phone_number = %s WHERE id = %s"""

        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cur:
                    conn.autocommit = True
                    if email != '' and name != '' and surname != '':
                        cur.execute(upd_name_surname, [name, surname, client_id])
                        cur.execute(upd_email, [email, client_id])
                        cur.execute(upd_phone_number, [phone_number, client_id])
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на обновление данных, соединение с PostgreSQL закрыто')

    # Удалить данные клиента
    def delete(self, client_id):

        del_email = """DELETE FROM Emails WHERE id = %s"""

        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cur:
                    conn.autocommit = True
                    cur.execute(del_email, [client_id])
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на удаление данных, соединение с PostgreSQL закрыто')

    # Добавить/удалить данные телефона(ов) клиента
    def upd_phone_number(self, client_id, phone_number='', mode=''):
        if phone_number == '' or mode not in ['del', 'add']:
            return
        else:
            if mode == 'del':
                upd_phone_number = """DELETE FROM Phones WHERE id = (SELECT id FROM Phones WHERE client_id = %s AND phone_number = %s)"""
            elif mode == 'add':
                upd_phone_number = """INSERT INTO Phones (client_id, phone_number) VALUES (%s, %s)"""
        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(upd_phone_number, [client_id, phone_number])
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на удаление/добавления данных № телефона, соединение с PostgreSQL закрыто')

    # Найти клиента по его данным: имени, фамилии, email или телефону.
    def select(self, search_request = [None, None, None, None]):

        sql = """SELECT c.id, c.name, c.surname, e.email, p.phone_number FROM Clients c
                                   FULL JOIN Phones p ON p.client_id = c.id
                                   JOIN Emails e ON e.id = c.id
                                  WHERE email=COALESCE(%s, email)
                                    AND name=COALESCE(%s, name)
                                    AND surname=COALESCE(%s, surname)
                                    AND phone_number=COALESCE(%s, phone_number)"""

        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    conn.autocommit = True
                    cur.execute(sql, search_request)
                    result = cur.fetchall()
        except (Exception, Error) as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if conn:
                conn.close()
                logging.info(f'Выполнен запрос на выборку данных, соединение с PostgreSQL закрыто')
                return result
