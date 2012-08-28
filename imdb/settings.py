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
import os

cwd = os.getcwd()

BOT_NAME = 'imdb'
BOT_VERSION = '0.0.1'

SPIDER_MODULES = ['imdb.spiders']
NEWSPIDER_MODULE = 'imdb.spiders'
DEFAULT_ITEM_CLASS = 'imdb.items.ImdbItem'

IMAGES_STORE = cwd + '/imdb/covers'
IMAGES_EXPIRES = 180 # 180 days

ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'imdb.scrapymysqldb.MySQLPipeline',
]
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#database settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'power'
DB_NAME = 'IMDB'
DB_TABLE = 'movies'

