import lxml.html as html 
import requests

from load_pages import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        
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
        link_list = []
        for link in self._select(self._queries['article_links']):
            if link:
                link_list.append(link)
        # review this i think dont need the link.has_attr
        return link_list

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
    