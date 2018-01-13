import csv
import logging
import urlparse

import scrapy
from scrapy.http.request import Request

# Only logging will print to console in Scrapy. "print" will not work.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CharityCharitiesSpider(scrapy.Spider):

    # "scrapy crawl" command line takes "name" as argument
    name = 'charity-charities-spider'

    def __init__(self, country, *args, **kwargs):
        """Add country as an instance variable. Use "-a" option with scrapy crawl and runspider to pass this argument."""
        super(CharityCharitiesSpider, self).__init__(*args, **kwargs)

        self.country = country

        self.url_base = 'http://www.charity-charities.org'
        # put slash here because rpartition function extracts it like this (when checking page type in is_city_page, is_country_page, etc.)
        self.url_path = '/{0}-charities'
        self.url_page = '{0}.html'
        self.output_file_path = '../output-{0}.csv'.format(self.country)

    def start_requests(self):
        """This is the starting point of a spider in Scrapy. It's on override of scrapy.Spider.start_requests"""
        url = self.url_base + \
            self.url_path.format(self.country) + '/' + \
            self.url_page.format(self.country)
        yield Request(url, self.parse)

    def parse(self, response):
        """Callback for parsing responses from each downloaded URL. This function yields the next URL to download."""

        # Detect if nonprofit page first, if its the final page just parse it!
        if self.is_nonprofit_page(response):
            logger.info('Parsing non profit page {0} ...'.format(
                urlparse.urlparse(response.request.url).path.rpartition('/')[2]))
            return self.parse_nonprofit_page(response)

        # if it's a country page (there are other country links such as Environmental/<Coutnryname>.html)
        if self.is_country_page(response.request.url):
            logger.info('Parsing country page ...')
            # return statement will forward the yielded generator from parse_country_page
            return self.parse_country_page(response)
        # if it's a city page (there are other city links such as <Countryname>-volunteers)
        elif self.is_city_page(response.request.url):
            logger.info('Parsing city page {0} ...'.format(
                urlparse.urlparse(response.request.url).path.rpartition('/')[2]))
            return self.parse_city_page(response)

    def parse_country_page(self, response):
        """If this is the first (or country) page we yield the list of cities."""
        # Use cssselect to find all anchor tags of "nwslink" class and extract their "href" attribute
        next_pages = response.css('a.nwslink::attr(href)').extract()
        for next_page in next_pages:
            url = response.urljoin(next_page)
            # only crawl city sub-pages. There are other nwslink anchors that we must skip
            if self.is_city_page(url):
                # Yield the next url to download
                yield scrapy.Request(url, callback=self.parse)

    def parse_city_page(self, response):
        """Yield pagination of city page and yield detail page of non-profit."""
        # TODO implement page scrolling
        non_profits = response.css('a.ftdnme::attr(href)').extract()
        for next_page in non_profits:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

        # Page Scrolling detect next city page navigation
        if len(response.css('a.chmlink::attr(href)').extract()) > 0: # If there is a next page link
            next_city_page = response.css('a.chmlink::attr(href)').extract()[-1]
            next_page_text = response.css('a.chmlink::text').extract()[-1]

            if next_page_text == "Next >>":
                url_next = response.urljoin(next_city_page)
                yield scrapy.Request(url_next, callback=self.parse)

    def parse_nonprofit_page(self, response):
        """Extract and write information on non-profit org to CSV. Nothing to yield (nothing to scrape further)"""
        name = response.css('p.profnam::text').extract_first()
        description = response.css('p.proftxt::text').extract_first()
        website = response.css('a.profweb::text').extract_first()
        city = response.css('a.ftdlc::text').extract_first()

        # Collect and parse cause_area
        cause_area_collection = response.css('a.ftdcat::text').extract()
        cause_area_output = ''
        for cause_area in cause_area_collection:
            if cause_area != "View All":
                cause_area_output += cause_area + ","

        yield {
            'name': name.replace('"','').strip(),
            'country': self.country,
            'description': description.replace('"','').strip(),
            'website': website,
            'cause_area': cause_area_output,
            'city': city
        }

    def is_country_page(self, url):
        # Get first and last path elements in request URL to identify which page we downloaded
        r_parts = urlparse.urlparse(url).path.rpartition('/')
        last_path_element = r_parts[2]
        first_path_element = r_parts[0]
        return (
            last_path_element == self.url_page.format(self.country) and
            first_path_element == self.url_path.format(self.country)
        )

    def is_city_page(self, url):
        # Get first and last path elements in request URL to identify which page we downloaded
        r_parts = urlparse.urlparse(url).path.rpartition('/')
        last_path_element = r_parts[2]
        first_path_element = r_parts[0]
        return (
            last_path_element != self.url_page.format(self.country) and
            first_path_element == self.url_path.format(self.country)
        )

    def is_nonprofit_page(self, response):
        non_profits = response.css('a.dead::text').extract_first()
        if non_profits is None:
            return False
        else:
            return True
