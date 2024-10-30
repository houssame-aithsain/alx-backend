#!/usr/bin/env python3
""" LRUCache module for caching system """

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class inherits from BaseCaching with LRU caching
    """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add item to cache_data using LRU algorithm """
        if key is not None and item is not None:
            if key not in self.cache_data and len(self.cache_data) \
                    >= BaseCaching.MAX_ITEMS:
                lru_key = self.order.pop(0)
                del self.cache_data[lru_key]
                print("DISCARD:", lru_key)
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """ Retrieve item from cache_data by key """
        if key is None or key not in self.cache_data:
            return None
        # Move the accessed key to the end to mark it as recently used
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
