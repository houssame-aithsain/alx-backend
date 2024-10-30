#!/usr/bin/env python3
""" BasicCache module
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    def put(self, key, item):
        """put"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """get"""
        if key and key in self.cache_data:
            return self.cache_data[key]
