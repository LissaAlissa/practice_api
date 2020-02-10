from bs4 import BeautifulSoup

from tutbysitescraper import TUTbySiteScraper
from rbcsitescraper import RBCSiteScraper
from mkrusitescraper import MKRUSiteScraper


class SiteScraperFactory():     
    """Связь между скраперами и запросами"""
    def get_site(self, site):
        # Возвращает необходимый скрапер по запрорсу
            site_news = []
            if site == 'tut.by':
                site_news = TUTbySiteScraper().get_content()
            elif site == 'rbc.ru':
                site_news = RBCSiteScraper().get_content() 
            elif site == 'mk.ru':
                site_news =  MKRUSiteScraper().get_content()
            return site_news
       
       
    def get_all_news(self):
        # Возвращает все скраперы
            all_news = [
                TUTbySiteScraper().get_content()[:10],
                RBCSiteScraper().get_content()[:10],
                MKRUSiteScraper().get_content()[:10],
            ]
            return all_news
     
