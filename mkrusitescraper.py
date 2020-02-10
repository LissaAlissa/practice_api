from bs4 import BeautifulSoup

from sitescraper import get_html, SiteScraper


class MKRUSiteScraper(SiteScraper):  
    """Скрапер статей 'mk.ru'."""
    def __init__(self):
        self.url = 'https://www.mk.ru/news'

    def get_content(self):
        # Возвращает небоходимый нам контент
        soup = get_html(self.url)
        items = soup.find('ul', class_='news_list').find_all('li')[:20]
        articles = []
        for item in items:
            link = item.find('a').get('href')
            header = item.find('a').get_text(strip=True)
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
