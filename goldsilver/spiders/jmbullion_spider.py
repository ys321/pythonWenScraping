from scrapy.spiders import CrawlSpider

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import json
import html
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner


class JmbullionSpider(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'FEED_URI': 'jmbnew1.json',  
        'FEED_FORMAT': 'json',
    }
    name = "jmbullion-crawl"
    start_urls = [
        'https://www.jmbullion.com/silver/',
        'https://www.jmbullion.com/gold/',
        ]
    allowed_domains = ['jmbullion.com']

    listings_css = [
        '.menu-item',
    ]

    products_css = ['#tab1 .fluid']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, allow=('silver'), tags=('link', 'a')), callback='_parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_item(self, response):
        spec_css = '#tabs-specification .specification-detail tr'
        produdct_specs =  [f"{spec.css('td ::text').getall()[0].strip()}: {spec.css('td ::text').getall()[1].strip()}" for spec in response.css(spec_css)]
        product_name = response.css('.title-area h2::text').get()
        product_category = response.css('script:contains(category)').re_first("category':'(.*?)'")
        product_image = response.css('[property="og:image"] ::attr(content)').get()
        product_url = response.url
        product_description = response.css('[itemprop="description"] ::text').get()
        sku = response.css('#jm_modal_login ::attr(value)').get()
        price = 'out of stock'
        if not response.css('#outofstocktip'):
            price = response.css('.payment-section table:not(.card-image) tbody tr')[0].css('td::text')[1].get().strip()
        
        raw_product_specifications = response.css('.specification-detail tr')
        product_specifications = ""
        for raw_spec in raw_product_specifications:
            product_specifications += f"{raw_spec.css('td::text').get().strip()}: {raw_spec.css('td::text').getall()[-1].strip()} ";
        yield {
            "product_name": product_name,
            "product_url": product_url,
            "product_category": product_category,
            "product_specifications": "".join(produdct_specs),
            "product_image": product_image,
            "p[?12;4$yroduct_description": product_description,
            "sku": sku,
            "price": price,
            "scrap_from": "jmbullion.com",
            "product_website_image": response.urljoin(response.css('.logo ::attr(src)').get()),
            "product_specifications": product_specifications,
            "product_weight": "",
            "product_year": response.css('.specification-detail tr td:contains(Year) + td::text').get(),
            "product_type": "Silver" if "silver" in product_name.lower() else "Gold"
        }

# https://findbullionprices.com/dealers/
