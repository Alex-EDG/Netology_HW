import requests
import bs4
import re

class ParsingHabr:
    def __init__(self):
        self.url = 'https://habr.com/ru/articles/'

    def parsing(self):
        """
        Parsing data from preview page https://habr.com/ru/articles/\n
        return: parsed_date: [{
                            'datetime': article_datetime,
                            'title': article_title,
                            'link': article_link,
                            'text': article_text
                            }]
        """
        response = requests.get(self.url)
        soup = bs4.BeautifulSoup(response.text, features='lxml')
        articles_list = soup.find_all('article', class_='tm-articles-list__item')
        parsed_data = []
        for article in articles_list:
            article_link = ('https://habr.com' + article.find('a', class_='tm-title__link')['href'])
            response = requests.get(article_link)
            soup = bs4.BeautifulSoup(response.text, features='lxml')
            article_title = soup.find('h1', class_='tm-title tm-title_h1').text.strip()
            article_datetime = soup.find('time')['title']
            # Время публикации статьи (Версия 2)
            # from datetime import datetime
            # article_datetime_iso = soup.find('time')['datetime']
            # article_datetime = datetime.fromisoformat(article_datetime).strftime('%d-%m-%Y %H:%M')
            article_text = soup.find('div', class_='tm-article-body').text.strip()
            parsed_data.append({
                              'datetime': article_datetime,
                              'title': article_title,
                              'link': article_link,
                              'text': article_text
                              })
        return parsed_data

def searh_by_keywords(data, keywords):
    """
    :param data: Data for keywords searching. Format:
    [{'datetime': article_datetime,
      'title': article_title,
      'link': article_link,
      'text': article_text }]
    :param keywords: List of keywords for search <List>
    :return: Print search results
    """
    for keyword in keywords:
        count = len(data)
        for idx, article_data in enumerate(data):
            num_of_ref = len(re.findall(keyword, article_data.get('text')))
            if num_of_ref and re.search(keyword, article_data.get('title')):
                print(f'Слово \033[94m{keyword}\033[0m встречается в названии статьи:\n'
                      f'<{article_data.get('datetime')[:10]}>-'
                      f'<{article_data.get('title')}>'
                      f'-<{article_data.get('link')}>\n'
                      f'Также в тексте статьи упоминается \033[92m{num_of_ref}\033[0m раз.\n'
                      f'-----------------')
            elif re.search(keyword, article_data.get('title')):
                print(f'Слово \033[94m{keyword}\033[0m встречается в названии статьи:\n'
                      f'<{article_data.get('datetime')[:10]}>-'
                      f'<{article_data.get('title')}>'
                      f'-<{article_data.get('link')}>\n-----------------')
            elif num_of_ref:
                print(f'Слово \033[94m{keyword}\033[0m встречается в тексте статьи:\n'
                      f'<{article_data.get('datetime')[:10]}>-'
                      f'<{article_data.get('title')}>'
                      f'-<{article_data.get('link')}>\n'
                      f'Упоминается \033[92m{num_of_ref}\033[0m раз.\n-----------------')

if __name__ == '__main__':

    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    ph = ParsingHabr()
    parsed_data_ = ph.parsing()
    searh_by_keywords(parsed_data_, KEYWORDS)