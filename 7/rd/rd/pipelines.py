# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SqlitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('crypto.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS crypto (
                name text,
                price text
            )
            """
        )
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """
            INSERT INTO crypto(name, price) values (?, ?)
            """, (item['name'], item['price'])
        )
        self.conn.commit()
        return item

