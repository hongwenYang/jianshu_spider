# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuSpiderPipeline:
    def __init__(self):
        dbparams = {
            'host': '172.16.10.30',
            'port': 3306,
            'user': 'root',
            'password': 'WC85roj5IfwOhIEK',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (
            item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],
            item['article_id']))
        self.conn.commit()

        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(title,content,author,avatar,pub_time,origin_url,article_id) values (%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '172.16.10.30',
            'port': 3306,
            'user': 'root',
            'password': 'WC85roj5IfwOhIEK',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(title,content,author,avatar,pub_time,origin_url,article_id) values (%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],item['article_id']))

    def handle_error(self, error, item, spider):
        print("=" * 10 + "error" + "=" * 10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)
