#!/usr/bin/env python3
"""
Contains the definition of the get_page function
"""
import redis
import requests
from functools import wraps
from typing import Callable


def cached(func: Callable) -> Callable:
    """
    Decorator that caches the results of the function call
    """
    redis = redis.Redis()

    @wraps(func)
    def wrapper(url):
        redis.incr(f"count:{url}")
        content = redis.get(f"content:{url}")
        if content:
            return content.decode("utf-8")
        content = func(url)
        redis.setex(f"content:{url}", 10, content)
        return content
    return wrapper


@cached
def get_page(url: str) -> str:
    """
    Obtain the html content of a particular URL and return it.
    Track how many times a URL was accessed in the key 'count: {url}'
    Cache the result with an expiration time of 10 seconds
    Args:
        url (str): url to be accessed
    Return:
        html content from the accessed url
    """
    response = requests.get(url)
    return response.text
