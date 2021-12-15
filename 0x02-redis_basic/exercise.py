#!/usr/bin/env python3
"""
Define a class Cache that deals with redis database operations
"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    name = method.__qualname__
    r = redis.Redis()
    inputs = r.lrange("{}:inputs".format(name), 0, -1)
    outputs = r.lrange("{}:outputs".format(name), 0, -1)
    res = zip(inputs, outputs)
    for i, o in res:
        print("{} -> {}".format(i, str(o)))


def call_history(method: Callable) -> Callable:
    """
    Takes a callable argument and returns a callable
    """
    @wraps(method)
    def history(self: redis.Redis, key: Union[str, int, float, bytes]) -> str:
        """
        Store history of inputs and outputs for a function
        """
        name = method.__qualname__
        self._redis.rpush("{}:inputs".format(name), key)
        result = method(self, key)
        self._redis.rpush("{}:outputs".format(name), result)
        return result
    return history


def count_calls(method: Callable) -> Callable:
    """
    Takes a callable argument and returns a callable
    """
    @wraps(method)
    def counter(self: redis.Redis, key: Union[str, int, float, bytes]) -> str:
        """
        Count howm many times a method is called
        """
        self._redis.incr(method.__qualname__)
        return method(self, key)
    return counter


class Cache:
    """
    Create an instance of a Redis client and flush it using flushdb
    """
    def __init__(self):
        """
        Create an instance of a Redis client and flush it using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self: redis.Redis, data: Union[str, int, float, bytes]) -> str:
        """
        Stores data in Redis with a randomly-generated key and returns the key
        Args:
            data (str, bytes, int, float): data to be stored
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self: redis.Redis, key: str, fn: Callable = None):
        """
        Makes a get request to Redis using the provided key and converts the
        result to the desired format using the function passed
        Args:
            key (str): key whose value is to be retrieved
            fn (callable): function to convert returned value to desired format
        """
        val = self._redis.get(key)
        if fn is not None:
            val_conv = fn(val)
            return val_conv
        return val
