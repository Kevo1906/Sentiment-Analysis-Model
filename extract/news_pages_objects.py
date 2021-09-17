import lxml.html as html 
import requests
import datetime

from load_pages import config
from utilities import date_formating

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        try:
            self._next_button = self._config['queries']['next_button']
        except KeyError:
            self._next_button = None
        self._dates = self._config['queries']['dates']
        
        self._visit(self._url)

    def _select(self, quey_string):
        return self._html.xpath(quey_string)

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()

        self._html = html.fromstring(response.content.decode('utf_8'))

class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
        
    @property
    def article_links(self):
        link_list = self._select(self._queries['article_links'])
        if self._next_button:
            today_date = str(datetime.date.today())
            
            while date_formating(self._select(self._dates)[-1]) == today_date:
                next_button = self._select(self._next_button)
                self._visit(next_button[0])
                link_list.extend(self._select(self._queries['article_links']))
        
        clean_link_list = []    
        for link in link_list:
            if link:
                clean_link_list.append(link)
        
        return clean_link_list

class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0]

    @property
    def url(self):
        return self._url
    
    @property
    def date(self):
        result = self._select(self._queries['article_date'])
        return result[0]
    