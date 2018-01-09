from scrapy.crawler import CrawlerProcess

from spiders.charity_charities_org import CharityCharitiesSpider


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CharityCharitiesSpider(country='Thailand'))
    process.start()
