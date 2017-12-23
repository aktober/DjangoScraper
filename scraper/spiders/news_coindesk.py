import scrapy

from app.models import NewsModel
from scraper.items import NewsItem

MAX_PAGES = 3


class CoinDeskSpider(scrapy.Spider):
    name = "coindesk"
    curr_page = 1

    def start_requests(self):
        NewsModel.objects.filter(source__icontains='coindesk').delete()
        urls = [
            'http://www.coindesk.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for l in response.css('div.article'):
            featured = l.css('div.article-featured').extract_first()
            item = NewsItem()
            if featured:
                item['title'] = l.css('div.article-meta > h3::text').extract_first()
                # item['pub_date'] = l.css('p.timeauthor > time::attr(datetime)').extract_first()
                item['description'] = 'some description'
                item['source'] = 'coindesk'
                item['image_url'] = l.css('div.subfeatured-picture > img::attr(src)').extract_first()
                item['featured'] = True
            else:
                item['title'] = l.css('h3 > a::text').extract_first()
                # item['pub_date'] = l.css('p.timeauthor > time::attr(datetime)').extract_first()
                item['description'] = 'some description'
                item['source'] = 'coindesk'
                item['image_url'] = l.css('img.wp-post-image::attr(src)').extract_first()
                item['featured'] = False
            item.save()

        # Pagination
        self.curr_page += 1
        next = 'http://www.coindesk.com/page/' + str(self.curr_page) + '/'
        if next and self.curr_page <= MAX_PAGES:
            yield scrapy.Request(url=next, callback=self.parse)
        print('finished')
