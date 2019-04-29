import scrapy
from scrapy import Request
#from scrapy.http import TextResponse as response

class hotpads_spider(scrapy.Spider):
	name = 'hotpad_snapshot'
	base = ["https://www.hotpads.com"]
	
	#Get all listings that are for rent by owner
	start_urls = ["https://www.hotpads.com/portland-or/for-rent-by-owner?isListedByOwner=true&lat=45.5659&lon=-122.6507&z=11"]
	

	
	def parse(self, response):
		links = response.xpath('//div[@class="SeoFooterLinks-link Utils-text-overflow"]//a/@href').getall()
		
		for link in links:
			absolute_url = self.base[0] + link
			#print(absolute_url)
			yield scrapy.Request(absolute_url,callback=self.parse_meta)
		
		#get the next page of results
		#next_page_url = response.xpath('//a[@class="Linker PagerItem"]/@href').extract()
		#next_absolute_url = response.urljoin(next_page_url)
		
		#yield scrapy.Request(next_absolute_url, callback = self.parse)
	
	def parse_meta(self,response):
		try:
			median_rent = response.xpath('//td[@class="AreaMarketInfo-table-data"]//text()')[0].get()
			monthly_chng = response.xpath('//td[@class="AreaMarketInfo-table-data"]//text()')[1].get()
		#location = response.css(query = (" div.ExploreWrapper > div > div.Title.ExploreWrapper-title.Title-lg")[0].css("*::text").get())
		except IndexError:
			median_rent = 'null'
			monthly_chng = 'null'
		location = response.xpath('//div[@class="Title ExploreWrapper-title  Title-lg"]/text()').get()
		yield {
		'location':location,
		'median_rent' : median_rent , 
		'monthly_chng':monthly_chng
		}