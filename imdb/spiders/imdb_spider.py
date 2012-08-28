# -*- coding: utf-8 -*-
# Copyright (C) 2012 Dairon Medina Caro <dairon.medina@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
import re

from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from imdb.items import ImdbItem

class ImdbSpider(CrawlSpider):
    name = 'imdb_toplist'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/chart/[\d]+s$'), callback='parse_toplist_page', follow=True),
    )

    def parse_toplist_page(self, response):
        hxs = HtmlXPathSelector(response)

        log.msg(hxs.select('//title/text()').extract().pop(0), level=log.INFO)

        # items = []

        rows = hxs.select('//div[@id="main"]/table[1]/tr')

        for row in rows[1:]:
            cols = row.select('.//td')

            if len(cols) is 0: break;

            # lets go deeper and get the rest of the movie data
            url = cols[2].select('.//a/@href').extract().pop(0)
            if url[0:4] != 'http':
                url = 'http://www.imdb.com'+url
            yield Request(url, callback=self.parse_movie_page)

    def parse_movie_page(self, response):
        hxs = HtmlXPathSelector(response)

        title_h1 = hxs.select('//h1[@class="header"]')
        year = title_h1.select('span/a/text()').extract().pop(0)

        ratings = hxs.select('//div[@class="star-box-details"]')

        item = ImdbItem()

        url = response.url
        if url[0:4] != 'http':
            url = 'http://www.imdb.com'+url

        id = re.search('(\d+)', url).group()
        item['id'] = int(id) if id else 0

        item['url'] = url
        item['title'] = title_h1.select('text()').re('.*[^<]').pop(1)

        item['year'] = int(year)

        description = hxs.select('//p[@itemprop="description"]/text()').extract()
        item['description'] = description.pop(0).strip() if description else ''

        cover = hxs.select('//td[@id="img_primary"]/a/img/@src').extract()

        rating = ratings.select('.//span[@itemprop="ratingValue"]/text()').extract().pop(0).strip()
        item['rating'] = float(rating) if ratings else 0.00

        votes = ratings.select('.//span[@itemprop="ratingCount"]/text()').extract().pop(0).replace(',', '').strip()
        item['votes'] = int(votes) if votes else 0

        # for ImagePipeline
        item['image_urls'] = cover if cover else []

        return item
