import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[a-z0-9]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        # item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        title = response.xpath("//h1[@class='_1RuRku']/text()").get().strip()
        avatar = response.xpath("//a[@class='_1qp91i _1OhGeD']/img/@src").get()
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        url = response.url
        # 根据?分割url
        url1 = url.split('?')[0]
        article_id = url1.split('/')[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()
        item = ArticleItem(
            title=title,
            author=author,
            avatar=avatar,
            article_id=article_id,
            pub_time=pub_time,
            origin_url=response.url,
            content=content
        )
        yield item
