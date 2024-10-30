#!/usr/bin/env python3
""" BasicCache module for caching system """

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class inherits from BaseCaching with no item limit """

    def put(self, key, item):
        """ Adds item to cache_data dictionary with key as identifier """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Returns the item linked to key in cache_data """
        return self.cache_data.get(key) if key is not None else None
