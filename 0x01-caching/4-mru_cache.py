#!/usr/bin/env python3
""" MRUCache module for caching system """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class inherits from BaseCaching with MRU caching """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add item to cache_data using MRU algorithm """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.order.pop()
                del self.cache_data[mru_key]
                print("DISCARD:", mru_key)
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """ Retrieve item from cache_data by key """
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
