import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from ebot.items import ProductItem
from ebot.items import ReviewItem

class ebaySpider(CrawlSpider):
    name = 'ebay'
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/Digital-Cameras-/31388/i.html']#['http://www.ebay.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('rpp',))),

        Rule(LinkExtractor(allow=('sch',))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('itm',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item =ProductItem()
        item['product_id'] = response.xpath('//div[@id="descItemNumber"]//text()').extract()[0]
        item['name'] = response.xpath('//h1[@id="itemTitle"]/text()').extract()[0]
        item['image'] = response.xpath('//div[@id="mainImgHldr"]//img[@itemprop="image"]/@src').extract()
        item['category'] = response.xpath('//ul//li[@class="bc-w"]//text()').extract()[0]
        item['url'] = response.url
        reviews=[]
        for r in response.xpath('//div[@class="rvws_container c-std"]//div[@id="rwid"]')[0:6]:
            review = ReviewItem(product_id=item['product_id'],product_name=item['name'],product_image=item['image'])
            review['user_review']=r.xpath('.//div[@itemprop="reviewBody"]//text()').extract()[0]
            reviews.append(review)
        item['reviews']=reviews
        return item
