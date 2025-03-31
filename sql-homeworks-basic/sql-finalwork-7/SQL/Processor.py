import random
import json
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, ArgumentError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from SQL.Models import create_tables, Base, Users, Words, UsersWords
from App.Common import Config
import logging

class SqlProcessor:
    """
    Crate connection to DB and loging process of data exchange.
    """
    def __init__(self):
        config = Config('settings.ini')
        dsn = (f"{config.read_config()['SQL_Alchemy']['dialect']}:"
               f"//{config.read_config()['SQL_Alchemy']['user']}"
               f":{config.read_config()['SQL_Alchemy']['password']}"
               f"@{config.read_config()['SQL_Alchemy']['host']}"
               f":{config.read_config()['SQL_Alchemy']['port']}"
               f"/{config.read_config()['SQL_Alchemy']['db_name']}")

        self.engine = sqlalchemy.create_engine(dsn)
        session = sessionmaker(bind=self.engine)
        self.session = session()

        logging.basicConfig(
                           level=logging.INFO,
                           filename='../logs.log',
                           filemode='a',
                           format='[%(asctime)s] %(levelname)s - %(message)s'
                           )

    # Создание структуры БД (таблиц)
    def create_tables(self):
        """
        Create DB structure accordance with scheme in Models
        """
        Base.metadata.create_all(self.engine)
        logging.info(f'Выполнен запрос на создание БД (таблиц), соединение с PostgreSQL закрыто')

    # Создание структуры БД (таблиц) и заполнение данными из файла в JSON формате
    def import_user_data(self):
        """
        ONLY for firstly fill data to DB
        Data import from **Data/import.json**\n
        Examples: [{"model": "users", "fields": {"name": "username"}}]
        """
        create_tables(self.engine)

        with open('../Data/import.json', 'r', encoding='utf-8') as fd:
            data = json.load(fd)
        try:
            for record in data:
                model = {
                    'users': Users,
                    'words': Words,
                    'users_words': UsersWords,
                }[record.get('model')]
                self.session.add(model(**record.get('fields')))

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
            self.session.rollback()
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
            self.session.rollback()
        except InvalidRequestError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
            self.session.rollback()
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнен запрос на заполнение БД данными из Data/import.json,'
                             f' соединение с PostgreSQL закрыто')

    # Вывести случайных 4 слова (с переводом) изучаемых текущим пользователем.
    def select_4_random_words(self, user_name=''):
        """
        :param user_name: <Str>
        :return: result: {'translate_word': '...', 'target_word': '...', 'other_words': ['..., '...', '...']} <Dict>
        """
        result = None
        try:
            query = self.session.query(Words.ru_word, Words.en1_word, Words.en2_word).select_from(UsersWords)
            query = query.join(Users, Users.id == UsersWords.id_user)
            query = query.join(Words, Words.id == UsersWords.id_word)
            select_results = query.filter(Users.name == user_name).order_by(func.random()).limit(4).all()
            target_w = select_results[3][1]
            translate_w = select_results[3][0]
            other_w = []
            for idx, item in enumerate(select_results):
                if idx < 3:
                    if item[2]:
                        other_w.append(item[2])
                        other_w.append(item[1])
                    else:
                        other_w.append(item[1])
            random.shuffle(other_w)
            result = {'translate_word': translate_w, 'target_word': target_w, 'other_words': other_w[:3]}

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнен запрос на выборку данных из БД для User={user_name},'
                             f' соединение с PostgreSQL закрыто')
            return result

    # Добавить слово (с переводом) в изучаемые текущим пользователем.
    def add_word(self, user_name, ru_wrd, en1_wrd, en2_wrd=None):
        """
        :param user_name: <Str>
        :param ru_wrd: <Str>
        :param en1_wrd: <Str>
        :param en2_wrd: <Str> Not obligatory
        """
        try:
            # Проверка наличия добавляемого слова в Words.
            id_wrd = self.session.query(Words.id).filter(Words.ru_word == ru_wrd).first()
            if id_wrd:
                id_wrd = id_wrd[0]
            else:
                data_1 = Words(ru_word=ru_wrd, en1_word=en1_wrd, en2_word=en2_wrd)
                self.session.add(data_1)
                self.session.commit()
                self.session.refresh(data_1)
                id_wrd = data_1.id
            id_usr = self.session.query(Users.id).select_from(Users).filter(Users.name == user_name)
            data_2 = UsersWords(id_user=id_usr, id_word=id_wrd)
            self.session.add(data_2)

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнен запрос на внесение данных (слова) в БД для User={user_name},'
                             f' соединение с PostgreSQL закрыто')

    # Удалить слово (с переводом) из изучаемых текущим пользователем.
    def delete_word(self, user_name, ru_wrd):
        """
        :param user_name: <Str>
        :param ru_wrd: <Str>
        """
        try:
            id_wrd = self.session.query(Words.id).filter(Words.ru_word == ru_wrd).first()
            if id_wrd:
                id_wrd = id_wrd[0]
            else:
                id_wrd = 0

            id_usr = self.session.query(Users.id).filter(Users.name == user_name).first()
            if id_usr:
                id_usr = id_usr[0]
            else:
                id_usr = 0

            id_userswords = self.session.query(UsersWords.id).filter(
                UsersWords.id_word == id_wrd and UsersWords.id_user == id_usr).first()
            if id_userswords:
                id_userswords = id_userswords[0]
            else:
                id_userswords = 0

            if id_wrd and id_userswords:
                item = self.session.query(UsersWords).filter(UsersWords.id == id_userswords).one()
                self.session.delete(item)
                response = 'успешно выполнен'
            else:
                response = 'не выполнен - в БД не найдено слово'

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнение запроса на удаление данных (слова) из БД для User={user_name},'
                             f'{response}, соединение с PostgreSQL закрыто')

    # Подсчёт числа слов изучаемых текущим пользователем.
    def count_words(self, user_name):
        """
        :param user_name: <Str>
        :return: count: <Int>
        """
        try:
            query = self.session.query(UsersWords.id_word).select_from(UsersWords)
            query = query.join(Users, Users.id == UsersWords.id_user)
            query = query.join(Words, Words.id == UsersWords.id_word)
            count = query.filter(Users.name == user_name).count()

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнен запрос на подсчёт слов в БД для User={user_name},'
                             f'найдено {count} слов, соединение с PostgreSQL закрыто')
            return count