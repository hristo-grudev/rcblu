import scrapy

from scrapy.loader import ItemLoader
from ..items import RcbluItem
from itemloaders.processors import TakeFirst


class RcbluSpider(scrapy.Spider):
	name = 'rcblu'
	start_urls = ['https://www.rcblu.com/en/about-rcb-in-luxembourg/news/']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="news"]/li[@class="news-item"]/a[1]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="modern-page-next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="news-detail"]/h3/text()').get()
		description = response.xpath('//div[@class="news-detail"]/div[@class="article"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="news-detail"]/p/text()').get()

		item = ItemLoader(item=RcbluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
