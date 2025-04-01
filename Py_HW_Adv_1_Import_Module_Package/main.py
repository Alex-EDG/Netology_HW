from datetime import datetime as dt
import requests
from application.salary import *
from application.db.people import *

class Accounting:
    def __init__(self):
        self.time_stmp = dt.now().strftime("%A, %d. %B %Y %H:%M")
        print(f'Сегодня: {self.time_stmp}\nДля персонала "{get_employees()}" выполняя "{calculate_salary()}"')

def fetch_open_meteo():
    response = requests.get('https://open-meteo.com/')
    if response.status_code == 200:
        print('Open-Meteo API is reachable.')
    else:
        print('Failed to reach Open-Meteo API.')

if __name__ == '__main__':

    clt = Accounting()

    fetch_open_meteo()