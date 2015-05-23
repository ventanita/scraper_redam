# -*- coding: utf-8 -*-
import re
import sys

import scrapy

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
            reason = 'Error: You need to enter an upper limit for record id to parse.'
            reason += '\n    scrapy crawl redam -a start_id=1 -a end_id=3000\n'
            print(reason)
            sys.exit(1)

    def start_requests(self):
        if self.start_id is None:
            start = 0
        else:
            start = self.start_id
        end = self.end_id
        scrapy.log.msg("Will scraping from record {} to {}".format(start, end), level=scrapy.log.INFO)

        for i in range(start, end + 1):
            url = 'http://casillas.pj.gob.pe/redamWeb/_rlvid.jsp.faces'
            url += '?_rap=pc_Index.obtenerDeudor&_rvip=/index.jsp&idDeudor=' + str(i)
            yield scrapy.Request(url, meta={'id': i})

    def parse(self, response):
        item = RedamItem()
        item['url'] = response.url
        item['given_names'] = get_given_names(response)
        item['paternal_surname'] = get_paternal_surname(response)
        item['maternal_surname'] = get_maternal_surname(response)
        item['dni'] = get_dni(response)
        item['debt'] = get_debt(response)
        item['bond'] = get_bond(response)
        with open(str(response.meta['id']) + '.html', 'w') as handle:
            handle.write(response.body)

        return item


def get_given_names(response):
    match = response.xpath('//span[contains(@id, "form1:text155")]/text()').extract()
    match = ''.join(match)
    return match.strip()


def get_paternal_surname(response):
    match = response.xpath('//span[contains(@id, "form1:text156")]/text()').extract()
    match = ''.join(match)
    return match.strip()


def get_maternal_surname(response):
    match = response.xpath('//span[contains(@id, "form1:text157")]/text()').extract()
    match = ''.join(match)
    return match.strip()


def get_dni(response):
    match = response.xpath('//span[contains(@id, "form1:text158")]/text()').extract()
    match = ''.join(match)
    return match.strip()


def get_debt(response):
    match = response.xpath('//span[contains(@id, "textNimpadeudado1")]/text()')
    amount = 0
    for i in match:
        amount += to_number(i.extract())
    return amount


def to_number(string):
    x = string.replace(",", "")
    x = float(x)
    return x


def get_bond(response):
    bonds = []
    selectors = response.xpath('//span[contains(@id, "form1:tableEx")]').re('[0-9]:[0-9]:tableEx4.0.+')
    for sel in selectors:
        if 'vinculo' in sel:
            try:
                bond_type = re.search('>(.+)<', sel).groups()[0]
            except KeyError:
                return None
        if 'Nombre' in sel:
            try:
                full_name = re.search('>(.+)<', sel).groups()[0]
            except KeyError:
                return None
            dictionary = {'bond_type': bond_type, 'full_name': full_name}
            if dictionary not in bonds:
                bonds.append(dictionary)
    return bonds
