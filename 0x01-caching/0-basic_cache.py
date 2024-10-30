#!/usr/bin/env python3
"""
BasicCache module
"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """basicCache"""

    def put(self, key, item):
        """put"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """get"""
        return self.cache_data.get(key, None)
