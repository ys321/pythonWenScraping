from scrapy.spiders import CrawlSpider
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import json
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner

class FindbullSpiderSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
    }
    name = "new"
    start_urls = ["https://findbullionprices.com/dealers/"]

    products_css = ['body .main']
    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse'),
    )

    def parse(self, response):
        companies = response.css('.deal-vendor-h3 a')
        for company in companies:
            company_name = company.css('::text').get().strip()
            company_url = company.css('::attr(href)').get()
            yield response.follow(company_url, self.parse_company, meta={'company_name': company_name})

    def parse_company(self, response):
        company_name = response.meta['company_name']
        rating = response.css('.dealer-rating::text').get()
        following_button = response.xpath('//button[@id="following"]')
        if following_button:
            following_url = following_button.xpath('../@href').get()
            yield response.follow(following_url, self.parse_following, meta={'company_name': company_name})
        else:
            following_url = None

    def parse_following(self, response):
        company_name = response.meta['company_name']
        table_rows = response.css('.table.table-responsive.table-striped tr')
        heading = response.css('#tab3 h2::text').get()
        for row in table_rows:
            product_name = row.css('td:first-child a::text').get()
            product_url = row.css('td:nth-child(1) a::attr(href)').get()

            yield response.follow(product_url, self.product_details, meta={'company_name': company_name, 'product_name': product_name, 'heading': heading})
    def product_details(self, response):
        company_name = response.meta['company_name']
        product_name =  response.meta['product_name']
        heading = response.meta['heading']
        table_rows = response.css('.table.table-responsive.table-striped tr')
        product_image_src = response.css('.product-details .product-image::attr(src)').get()

        weight = None
        country = None
        first_word = None
        last_word = None
        # Extract weight and country from the specifications section
        specifications = response.css('.text-left:nth-child(4) table tr')
        arr1 = []
        for spec in specifications:
            value123 = spec.css('td:nth-child(2)::text').get()
            # label123 = spec.css('td:first-child::text').get()
            # arr1.append(label123)
            arr1.append(value123)
            
            # for string1 in arr1[2]:
        type1 = arr1[2].split()
        last_word = type1[-1]
        first_word = type1[0]
            #    'Weight '=  weight = value.strip()
            # 'Country'=  country = value.strip()

        for row in table_rows:
            dealer = row.css('td:nth-child(1) a::text').get()
            price = row.css('td:nth-child(3)::text').get(default='').strip()
            dealer_premium = row.css('td:nth-child(5)::text').get(default='').strip()
            company_link = row.css('td.dealer-link a::attr(href)').get(default='').strip()

            product_image_src = response.css('.product-details .product-image::attr(src)').get()
            if product_image_src:
                image_url = response.urljoin(product_image_src)
                image_name = os.path.basename(image_url)
                image_path = os.path.join('images', image_name)

                yield {
                    'company_name': company_name,
                    'product_name': product_name.strip() if product_name else None,
                    'head': heading,
                    'dealer': dealer,
                    'price': price,
                    'dealer_premium': dealer_premium,
                    'link': company_link,
                    'image_src': product_image_src,
                    'image_path': image_path,
                    'weight': arr1[0],
                    'type': last_word,
                    'metal': first_word,
                    'category': first_word,
                    'Collections': arr1[0] + first_word + ' ' + last_word,
                }

                # Request to download the image
                yield scrapy.Request(url=image_url, meta={'image_path': image_path}, callback=self.save_image)

    def save_image(self, response):
        image_path = response.meta['image_path']
        with open(image_path, 'wb') as f:
            f.write(response.body)