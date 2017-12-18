from datetime import datetime, timedelta
import scrapy
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.mail import MailSender

mailer = MailSender.from_settings(settings)

class CebSale(scrapy.Item):
    tags = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "tweets_cebpac"

    def start_requests(self):
        urls = [
            'https://twitter.com/CebuPacificAir?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for tweet in response.css('div.js-tweet-text-container'):
            item = CebSale()
            sale = tweet.xpath('//a[contains(@href, "CEBSeatSale")]/@href')
            
            if(len(sale) > 0):
                item['tags'] = tweet.xpath('//a[contains(@href, "CEBSeatSale")]/@href').extract()
                item['time'] = tweet.xpath('//a[contains(@href, "/CebuPacificAir/status/")]//span/@data-time').extract_first()
                item['date'] = tweet.xpath('//a[contains(@href, "status")]/@data-original-title').extract()
                item['link'] = tweet.css('span.js-display-url').extract()
                
                yield item

        for link in response.css('li.next a'):
            yield response.follow(link, callback=self.parse)


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(QuotesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished
        