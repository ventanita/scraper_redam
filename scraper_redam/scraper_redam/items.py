# -*- coding: utf-8 -*-

# Copyright 2015 by AniversarioPeru. All rights reserved.
# This code is part of the Ventanita distribution and governed by its
# license. Please see the LICENSE file that should have been included
# as part of this package.

import scrapy


class RedamItem(scrapy.Item):
    given_names = scrapy.Field()
    maternal_surname = scrapy.Field()
    paternal_surname = scrapy.Field()
    dni = scrapy.Field()
    url = scrapy.Field()
    debt = scrapy.Field()
    bond = scrapy.Field()  # person that is owed money, most of the time is a child.
