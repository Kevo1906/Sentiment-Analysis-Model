import argparse
import csv
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

import news_pages_objects as news
from load_pages import config

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def news_scraper(news_site_uid):
    hosts = config()['sites'][news_site_uid]['url']
    print(hosts)
    articles = []
    if type(hosts) is list:
        for host in hosts:
            logging.info(f'Beginning scraper for {host}')
            homepage = news.HomePage(news_site_uid, host)

            for link in homepage.article_links:
                article = fetch_article(news_site_uid, host, link)

                if article:
                    logger.info('Article fetched!!')
                    articles.append(article)
    else:
        logging.info(f'Beginning scraper for {hosts}')
        homepage = news.HomePage(news_site_uid, hosts)

        for link in homepage.article_links:
            article = fetch_article(news_site_uid, hosts, link)

            if article:
                logger.info('Article fetched!!')
                articles.append(article)

    save_articles(news_site_uid, articles)

def save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{news_site_uid}_{now}_articles.csv'
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    

    with open(f'./data/{out_file_name}', mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop))for prop in csv_headers]
            writer.writerow(row)

def fetch_article(news_site_uid, host, link):
    logger.info(f'Start fetching article at {link}')

    article= None
    
    try:
        article = news.ArticlePage(news_site_uid,build_link(host,link))
        
    except (HTTPError, ConnectionError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None
    
    return article

def build_link(host, link):
    # Fixing the urls if host and link have repeating parts
    if not is_well_formed_link.match(link):
        if host.split("/")[-1] == link.split("/")[1]:
            link= link.split("/")
            link.pop(0)
            link.pop(0)
            fix_link = ""
            for l in link:
                fix_link+= "/" + l
            link = fix_link
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    news_scraper(args.news_site)                    
     