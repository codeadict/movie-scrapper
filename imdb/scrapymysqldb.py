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
"""Scrapy pipeline to store crawled items on MySQL Database"""

__author__ = 'Dairon Medina Caro <dairon.medina@gmail.com>'
__version__ = '$Revision: 1.0 $'

#scrapy things
import re
import pymysql
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MySQLPipeline(object):
    def __init__(self):
        """"Init DB settings"""
        try:
            self.connection = pymysql.connect(host=settings['DB_HOST'], port=3306, user=settings['DB_USER'], passwd=settings['DB_PASS'], db=settings['DB_NAME'])
        except:
            log.msg("ERROR CONNECTING TO MYSQL", level=log.DEBUG)
        
    def process_item(self, item, spider):
        """Creates record on DB if not exist yet"""
        cursor = self.connection.cursor()
        #ignore item if not have an ID
        itemcol = item
        del itemcol['image_urls']
        item['image_large'] = item['images'][0]['path'][5:] if item['images'][0] else ''
        del itemcol['images']
    	keys = itemcol.keys()

        if 'id' not in keys:
            raise DropItem("Missing id field")


        if cursor.execute('SELECT `id` FROM `%s` WHERE `id` = %d' %(settings['DB_TABLE'], item['id'])):
            #Update if exist
            sql = 'UPDATE `%s` SET' % settings['DB_TABLE']
            i = 0
            for (key, value) in item.items():
                if key in ('images','image_urls'): continue
                sql += ', ' if i > 0 else ' '
                sql += '`%s` = %s' % (key, self.connection.escape(value))
                i += 1
            sql += ' WHERE id = %d' % item['id']
        else:
            #Insert new one
            sql = 'INSERT INTO `%s`' % settings['DB_TABLE']
            sql += ' (%s) VALUES (' % (', ').join(keys)
            i = 0
            for key in keys:
                if key in ('images','image_urls'): continue
                sql += ', ' if i > 0 else ' '
                sql += '%s' % self.connection.escape(item[key])
                i += 1
            sql += ')'

            log.msg(sql, level=log.DEBUG)

        cursor.execute(sql)

        cursor.close()

        return item
