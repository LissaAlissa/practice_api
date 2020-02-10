from bs4 import BeautifulSoup

from sitescraper import get_html, SiteScraper


class RBCSiteScraper(SiteScraper):  
    """Скрапер статей 'rbc.ru'."""
    def __init__(self):
        self.url = 'https://www.rbc.ru'

    def get_content(self):
        # Возвращает небоходимый нам контент
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

  