# -*- coding: utf-8 -*-
import scrapy

from scraper_redam.exceptions import MissingEndRecordId
from scraper_redam.items import RedamItem


class RedamSpider(scrapy.Spider):
    name = "redam"
    allowed_domains = ["casillas.pj.gob.pe"]

    def __init__(self, start_id='', end_id='', *args, **kwargs):
        super(RedamSpider, self).__init__(*args, **kwargs)
        try:
            self.start_id = int(start_id)
        except ValueError:
            self.start_id = None

        try:
            self.end_id = int(end_id)
        except ValueError:
            reason = 'You need to enter an upper limit for record id to parse.'
            reason += '\n    scrapy crawl redam -a start_id=1 end_id=3000\n'
            raise MissingEndRecordId(reason)

    def start_requests(self):
        if self.start_id is None:
            start = 0
        else:
            start = self.start_id
        end = self.end_id
        scrapy.log.msg("Will scraping from record {} to {}".format(start, end), level=scrapy.log.INFO)

        for i in range(start, end):
            url = 'http://casillas.pj.gob.pe/redamWeb/_rlvid.jsp.faces'
            url += '?_rap=pc_Index.obtenerDeudor&_rvip=/index.jsp&idDeudor=' + str(i)
            yield scrapy.Request(url, meta={'id': i})

    def parse(self, response):
        item = RedamItem()
        item['url'] = response.url
        with open(response.meta['id'] + '.html', 'w') as handle:
            handle.write(response.content)

        return item
