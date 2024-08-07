# utils.py
# to clear cache

from django.core.cache import cache

def clear_all_cache():
    cache.clear()