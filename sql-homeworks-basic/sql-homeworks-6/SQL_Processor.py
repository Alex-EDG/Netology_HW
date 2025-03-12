import json
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, ArgumentError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Base, Publisher, Shop, Book, Stock, Sale
from Common import Config
import logging

class SqlProcessor:
    def __init__(self):
        config = Config('settings.ini')
        dsn = (f"{config.read_config()['SQL_Alchemy']['dialect']}:"
               f"//{config.read_config()['SQL_Alchemy']['user']}"
               f":{config.read_config()['SQL_Alchemy']['password']}"
               f"@{config.read_config()['SQL_Alchemy']['host']}"
               f":{config.read_config()['SQL_Alchemy']['port']}"
               f"/{config.read_config()['SQL_Alchemy']['db_name']}")

        self.engine = sqlalchemy.create_engine(dsn)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        logging.basicConfig(
            level=logging.INFO,
            filename='logs.log',
            filemode='a',
            format='[%(asctime)s] %(levelname)s - %(message)s'
            )

    # Создание структуры БД (таблиц)
    def create_tables(self):

        Base.metadata.create_all(self.engine)
        logging.info(f'Выполнен запрос на создание БД (таблиц), соединение с PostgreSQL закрыто')

    # Создание структуры БД (таблиц) и заполнение данными из файла в JSON формате
    def fill_test_data(self):

        create_tables(self.engine)

        with open('fixtures/tests_data.json', 'r') as fd:
            data = json.load(fd)

        try:
            for record in data:
                model = {
                    'publisher': Publisher,
                    'shop': Shop,
                    'book': Book,
                    'stock': Stock,
                    'sale': Sale,
                }[record.get('model')]
                self.session.add(model(id=record.get('pk'), **record.get('fields')))

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
                logging.info(f'Выполнен запрос на заполнение БД данными из fixtures/tests_data.json, соединение с PostgreSQL закрыто')

    # Найти информацию о покупках книг определённого издателя.
    def querys(self, p_name = ''):

        result = None
        try:
            query = self.session.query(Book.title, Shop.name, Sale.price, func.to_char(Sale.date_sale, 'DD-MM-YYYY')).select_from(Sale)
            query = query.outerjoin(Stock, Stock.id == Sale.id_stock)
            query = query.join(Book, Stock.id_book == Book.id)
            query = query.outerjoin(Shop, Stock.id_shop == Shop.id)
            query = query.join(Publisher, Book.id_publisher == Publisher.id).filter(Publisher.name == p_name)
            result = query.all()

        except IntegrityError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        except ArgumentError as error:
            logging.critical(f'Ошибка при работе с PostgreSQL:{error}')
        finally:
            if self.session:
                self.session.commit()
                logging.info(f'Выполнен запрос на выборку данных из БД для Publisher={p_name},'
                             f' соединение с PostgreSQL закрыто')
                return result