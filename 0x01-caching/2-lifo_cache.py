#!/usr/bin/env python3
""" LIFOCache module for caching system """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class inherits from BaseCaching with LIFO caching """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """ Add item to cache_data using LIFO algorithm """
        if key is not None and item is not None:
            if key not in self.cache_data and \
                    len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.last_key:
                    del self.cache_data[self.last_key]
                    print("DISCARD:", self.last_key)
            self.cache_data[key] = item
            self.last_key = key

    def get(self, key):
        """ Retrieve item from cache_data by key """
        return self.cache_data.get(key)
