import requests
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractstaticmethod
import lxml


def get_html(url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


class SiteScraper(metaclass=ABCMeta):
    '''Абтрактный скрапер статей. '''

    @abstractstaticmethod
    def get_content():
        # Возвращает небоходимый нам контент
        pass