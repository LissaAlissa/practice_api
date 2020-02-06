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
    @abstractstaticmethod
    def get_content():
        """Scraper"""

class TUTbySiteScraper(SiteScraper):
    def __init__(self):
        self.url = 'https://tut.by'

    def get_content(self):
        soup = get_html(self.url)
        items = soup.find('div', id='title_news_block').find_all('a', class_='entry__link io-block-link')[:20]
        articles = []
        for item in items:
            link = item.get('href')
            main_article = get_html(link)
            header = ' '.join(main_article.find('div', {'class': 'b-article'}).find('h1').text.split())
            text_cont = []
            for cont in  main_article.find('div', attrs={'id': 'article_body'}).find_all('p'):
                if main_article.find('script', attrs={'type': "text/javascript"}):
                    main_article.script.decompose()
                if main_article.find('p', class_='Tweet-text'):
                    main_article.find('p', class_='Tweet-text e-entry-title').decompose()      
                text_cont.append(cont.get_text(strip=True).replace('\xa0', ' '))
                
            articles.append({ 
                'name': 'tut.by',
                'link': link,
                'header': header,  
                'text':  ' '.join(text_cont)      
            })
        return articles

class RBCSiteScraper(SiteScraper):  
    def __init__(self):
        self.url = 'https://www.rbc.ru'

    def get_content(self):
        soup = get_html(self.url)
        items = soup.find_all('div', class_='main__feed')[:20]
        articles = []
        for item in items:
            link = item.find('a', class_='main__feed__link').get('href')
            header = item.find('span', class_='main__feed__title').get_text(strip=True) 
            main_article = get_html(link)
            text_cont = []
            for cont in  main_article.find('div', class_='article__text').find_all('p'):
                text_cont.append(cont.get_text(strip=True).replace('\xa0', ' '))
            
            articles.append({
                'name': 'rbc.ru',
                'link': link,
                'header': header,
                'text':  ' '.join(text_cont)
            })
        return articles

        
class MKRUSiteScraper(SiteScraper):   
    def __init__(self):
        self.url = 'https://www.mk.ru/news'

    def get_content(self):
        soup = get_html(self.url)
        items = soup.find('ul', class_='news_list').find_all('li')[:20]
        articles = []
        for item in items:
            link = item.find('a').get('href')
            header = ' '.join(item.find('a').text.split())
            main_article = get_html(link)
            text_cont = []
            for cont in  main_article.find('div', class_='inread-content').find_all('p'):
                if main_article.find('strong'):
                    main_article.strong.decompose()
                text_cont.append(cont.get_text(strip=True).replace('\xa0', ' '))
            articles.append({
                'name':  'mk.ru',
                'link': link,
                'header': header,
                'text':  ' '.join(text_cont)
            })
        return articles


class SiteScraperFactory():     
    def get_site(self, site):
        try:
            site_news = []
            if site == 'tut.by':
                site_news = TUTbySiteScraper().get_content()
            elif site == 'rbc.ru':
                site_news = RBCSiteScraper().get_content() 
            elif site == 'mk.ru':
                site_news =  MKRUSiteScraper().get_content()
            return site_news
        except:
           return {'error': 'Not found'}
        
    
    def get_all_news(self):
       
            all_news = [
                TUTbySiteScraper().get_content(),
                RBCSiteScraper().get_content(),
                MKRUSiteScraper().get_content(),
            ]
            return all_news
     
