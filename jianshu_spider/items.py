# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    word_count = scrapy.Field()
    subjects = scrapy.Field()
    comment_count = scrapy.Field()
