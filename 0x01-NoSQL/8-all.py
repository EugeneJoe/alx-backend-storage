#!/usr/bin/env python3
"""
List all documents in a collection
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """List all documents in the collection"""
    col = mongo_collection.find({})
    if col:
        return col
    else:
        return []
