#!/usr/bin/env python3
""" FIFOCache module for caching system """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class inherits from BaseCaching with FIFO caching """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add item to cache_data using FIFO algorithm """
        if key is not None and item is not None:
            if key not in self.cache_data and len(self.cache_data) \
                    >= BaseCaching.MAX_ITEMS:
                first_key = self.order.pop(0)
                del self.cache_data[first_key]
                print("DISCARD:", first_key)
            self.cache_data[key] = item
            if key not in self.order:
                self.order.append(key)

    def get(self, key):
        """ Retrieve item from cache_data by key """
        return self.cache_data.get(key)
