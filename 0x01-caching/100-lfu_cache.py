#!/usr/bin/env python3
""" LFUCache module for caching system """

from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """ LFUCache class inherits from BaseCaching with LFU caching """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.frequency = defaultdict(int)
        self.order = []

    def put(self, key, item):
        """ Add item to cache_data using LFU algorithm """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.frequency.values())
                lfu_keys = [k for k, freq in self.frequency.items()
                            if freq == min_freq]

                if len(lfu_keys) > 1:
                    lru_key = min(lfu_keys, key=lambda k: self.order.index(k))
                else:
                    lru_key = lfu_keys[0]

                del self.cache_data[lru_key]
                del self.frequency[lru_key]
                self.order.remove(lru_key)
                print("DISCARD:", lru_key)

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order.append(key)

    def get(self, key):
        """ Retrieve item from cache_data by key """
        if key is None or key not in self.cache_data:
            return None
        self.frequency[key] += 1
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
