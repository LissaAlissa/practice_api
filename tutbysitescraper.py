from bs4 import BeautifulSoup

from sitescraper import get_html, SiteScraper


class TUTbySiteScraper(SiteScraper):
    """Скрапер статей 'tut.by'."""
    def __init__(self):
        self.url = 'https://tut.by'

    def get_content(self):
        # Возвращает небоходимый нам контент
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

# p = TUTbySiteScraper().get_content()
# sprint(p)