
from scrapy.spiders import CrawlSpider
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import json
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner

class FindbullSpiderSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  # Adjust download delay as needed
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Limit concurrent requests to avoid triggering anti-bot mechanisms
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
    }
    name = "findbull_spider123"
    # allowed_domains = ["findbullionprices.com"]
    start_urls = ["https://findbullionprices.com/"]

    products_css = ['body .main']
    rules = (
        # Rule(LinkExtractor(restrict_css=listings_css, tags=('link', 'a')), callback='_parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse'),
    )

    # def parse(self, response):
    #     # h2 = response.css('h2::text').get()
    #     # h3 = response.css('h3::text').get()
    #     # h2_tags = response.css('h3::text').getall()
    #     # table = response.css('#featured_table tbody tr').getall()
    #     # # for heading in h2_tags:
    #     # for row in table:
    #     #     # Extracting data from each row
    #     #     cells = row.css('td::text').getall()
    #     #     yield {
    #     #         'data': cells
    #     #     }
    #     table_rows = response.css('.col-md-12 table tbody tr')
    #     title = response.css('h3.ssp::text').getall()
    #     for row in table_rows:
    #         # Extracting data from each row
    #         product = row.css('td:nth-child(1) a::text').get()
    #         dealer = row.css('td:nth-child(2) .dealer-name::text').get()
    #         cheapest_price = row.css('td:nth-child(3) span::text').get()
    #         href = row.css('td:nth-child(1) a::attr(href)').get().lstrip('/')
    #         # table_title = title.get()

    #         yield {
    #             'product': product.strip() if product else None,
    #             'dealer': dealer.strip() if dealer else None,
    #             'cheapest_price': cheapest_price.strip() if cheapest_price else None,
    #             'url': response.url + href,
    #             'table_title' : title
    #         }
    def parse(self, response):
        titles = response.css('h3.ssp::text').getall()
        tables = response.css('.col-md-12 table')
        
        for title, table in zip(titles, tables):
            table_rows = table.css('tbody tr')
            for row in table_rows:
                # Extracting data from each row
                product = row.css('td:nth-child(1) a::text').get(default='').strip()
                dealer = row.css('td:nth-child(2) .dealer-name::text').get(default='').strip()
                cheapest_price = row.css('td:nth-child(3) span::text').get(default='').strip()
                href = row.css('td:nth-child(1) a::attr(href)').get(default='').lstrip('/')

                yield {
                    'product': product.strip() if product else None,
                    'dealer': dealer.strip() if dealer else None,
                    'cheapest_price': cheapest_price.strip() if cheapest_price else None,
                    'url': response.url + href,
                    'table_title': title
                }