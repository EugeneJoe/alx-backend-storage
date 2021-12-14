#!/usr/bin/env python3
"""
Return all students sorted by average score
"""


def top_students(mongo_collection):
    """
    return all students sorted by average score
    Args:
        mongo_collection: pymongo collection object
    """
    return mongo_collection.aggregate([
        {"$project": {
            'name': '$name',
            'averageScore': {'$avg': '$topics.score'}
        }
        },
        {"$sort": {'averageScore': -1}}
    ])
