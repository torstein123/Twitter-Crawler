import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field


class VergeReview(Item):
    url = Field()
    title = Field()
    author_name = Field()
    author_link = Field()


class VergeReviewsSpider(CrawlSpider):
    name = 'verge_reviews'
    allowed_domains = ['theverge.com']
    start_urls = ['https://www.theverge.com/reviews']
    rules = [
       Rule(LinkExtractor(allow=r'https://www.theverge.com/\d{4}/\d{1,2}/\d{1,2}/\d+/[^/]+$'), callback='parse_review')
    ]

    def parse_review(self, response):
        review = VergeReview()
        review['url'] = response.url
        review['title'] = response.css('h1::text').get()
        author_link = response.css('div.c-byline__item > a::attr(href)').get()
        author_name = response.css('div.c-byline__item > a::text').get()
        if not author_name or not author_link:
            # Extract author name and link from the <a> tag
            author_info = response.xpath('//a[contains(@href,"/authors/")]/text()')
            author_name = author_info.get()
            author_link = response.urljoin(author_info.xpath('../@href').get())
        review['author_name'] = author_name.strip() if author_name else None
        review['author_link'] = author_link if author_link else None
        yield review
