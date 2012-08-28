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
#
#
#  Description: Define here the models for your scraped items
from scrapy.item import Item, Field

class ImdbItem(Item):
    '''IMDB Movie Item'''
    id = Field()
    url = Field()
    title = Field()
    year = Field()
    description = Field()
    image_small = Field()
    image_large = Field()
    rating = Field()
    votes = Field()

    # need this in order to enable the ImagePipelin
    # this won't be persisted
    image_urls = Field()
    images = Field()
