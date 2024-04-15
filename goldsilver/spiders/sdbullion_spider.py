from scrapy.spiders import CrawlSpider

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import json
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner


class SdbullionSpider(CrawlSpider):
    
    name = "sdbullion-crawl"
    start_urls = [
        'https://sdbullion.com/gold',
        'https://sdbullion.com/silver',        
        ]
    allowed_domains = ['sdbullion.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
    }

    listings_css = [
        '.item-wrapper',
        '.pagebuilder-column span',

    ]

    products_css = ['.product-item-link']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, tags=('link', 'a')), callback='_parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_prouct'),
    )


    def parse_prouct(self, response):
        spec_css = '#product-attribute-specs-table tr'
        produdct_specs =  [f"{spec.css('th ::text').get().strip()}: {spec.css('td ::text').get().strip()}" for spec in response.css(spec_css)]
        product_name = response.css('[data-ui-id="page-title-wrapper"]::text').get()
        product_url = response.url
        product_category = " > ".join(response.css('.items [class*=category] a::text').getall())
        product_image = response.css('[property="og:image"] ::attr(content)').get()
        product_description = "".join(response.css('.description h2::text, .description p::text').getall())
        sku = response.css('[itemprop="sku"] ::attr(content)').get()
        price = response.css('.price-formatted::text').get()
        raw_product_specifications = response.css('#product-attribute-specs-table tr')
        product_specifications = ""
        for raw_spec in raw_product_specifications:
            product_specifications += f"{raw_spec.css('th::text').get()}: {raw_spec.css('td::text').get()}";
        yield {
            "product_name": product_name,
            "product_url": product_url,
            "product_category": product_category,
            "product_specifications": "".join(produdct_specs),
            "product_image": product_image,
            "product_description": product_description,
            "sku": sku,
            "price": price,
            "scrap_from": "sdbullion.com",
            "product_website_image": response.css('.logo-image::attr(src)').get(),
            "product_specifications": product_specifications,
            "product_weight": "",
            "product_year": response.css('#product-attribute-specs-table tr th:contains(Year) + td::text').get(),
            "product_type": response.css('#product-attribute-specs-table tr th:contains(Type) + td::text').get(),
        }






