import re
import scrapy

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from app.models import NewsModel
from scraper.items import NewsItem


PICTURES = ['i.imgur.com', 'imgur.com']
SELFMADE = ['i.reddit.it', 'self.Bitcoin']
BLOG = ['medium.com']
TWITTER = ['twitter.com']
MASSMARKET = ['theguardian.com', 'cnbc.com']

MAX_PAGES = 3


class RedditSpider(scrapy.Spider):
    name = "reddit"
    curr_page = 1

    def start_requests(self):
        NewsModel.objects.all().delete()
        urls = [
            'https://www.reddit.com/r/Bitcoin/top/?sort=top&t=week'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []

        for l in response.xpath('//div[@data-context="listing"]'):
            item = NewsItem()
            item['use_in_report'] = False
            item['title'] = l.css('a.title::text').extract_first()[:254]
            item['description'] = ''

            image_url = l.css('a.thumbnail img::attr(src)').extract_first()
            item['image_url'] = 'https:' + image_url if image_url else ''

            domain = l.css('span.domain a::text').extract_first()
            item['category'] = detect_category(domain)

            comments = l.css('a.bylink::text').extract_first()
            number = re.sub('[ comments]', '', comments)
            item['comments'] = int(number)

            votes = l.css('div.unvoted::text').extract_first()
            item['votes'] = get_vote_number(votes)

            item.save()
            items.append(item)

        # Pagination
        self.curr_page += 1
        next = response.css('span.next-button a::attr(href)').extract_first()
        if next and self.curr_page < MAX_PAGES:
            yield scrapy.Request(url=next, callback=self.parse)
        print('finished ' + str(self.curr_page) + ' page')


def get_vote_number(votes):
    if 'k' in votes:
        big_votes = re.sub('[k]', '00', votes)
        result = re.sub('[.]', '', big_votes)
        return int(result)
    return int(votes)


def detect_category(domain):
    if domain in PICTURES:
        return 'pictures'
    if domain in SELFMADE:
        return 'selfmade'
    if domain in BLOG:
        return 'blog'
    if domain in TWITTER:
        return 'twitter'
    if domain in MASSMARKET:
        return 'massmarket'
    return 'other: ' + domain


crawler = RedditSpider()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(crawler)
    reactor.stop()

crawl()
reactor.run()