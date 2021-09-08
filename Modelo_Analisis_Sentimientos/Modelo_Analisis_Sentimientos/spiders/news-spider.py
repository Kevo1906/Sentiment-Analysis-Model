import scrapy 
# from common import config
import datetime
class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://lapatria.bo/'
    ]
    custom_settings = {
        'FEED_URI': f'{datetime.date.today()}.csv',
        'FEED_FORMAT': 'csv'
        #'ROBOTSTXT_OBEY': True,
        #'FEED_EXPORT_ENCODING': 'utf-8',
        #'USER_AGENT': 'Padi19'
    }

    

    #def parse_articles(self, response):
    #    title = response.xpath('//div[@class="td-post-header"]//h1[@class="entry-title"]/text()').get()
    #    article = response.xpath('//div[@class="td-post-content tagdiv-type"]/p/text()').getall()
    #    yield {
    #        'title': title,
    #        'article': article
    #    }
    # This parse give urls of each new in the page
    def parse(self, response):
        todays_date = datetime.date.today()
        
        urls = response.xpath('//div[@class="td-block-span6"]//h3/a/@href').getall()
        news_dates = response.xpath('//div[@class="td-block-span6"]//span[@class="td-post-date"]/time/@datetime').getall()
        news_dates = list(map(lambda x: x.split("T")[0], news_dates))

        yield {
            'urls': urls,
            'news_dates': news_dates
        }

        #for url,news_date in urls,news_dates:
        #    if news_date == todays_date:
        #        yield response.follow(url, callback=self.parse_articles)