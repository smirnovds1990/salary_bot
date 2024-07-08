import json
from datetime import datetime as dt

from constants import DATETIME_FORMAT, GROUP_TYPES
from create_bot import db


def parse_data_from_message(text):
    data = json.loads(text)
    group_type = data['group_type']
    start = dt.strptime(data['dt_from'], DATETIME_FORMAT)
    stop = dt.strptime(data['dt_upto'], DATETIME_FORMAT)
    return start, stop, group_type


async def get_data_from_db(start, stop, group_type):
    type_to_group = GROUP_TYPES[group_type]
    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": start,
                    "$lte": stop
                }
            }
        },
        {
            "$group": {
                "_id": type_to_group,
                "total_value": {"$sum": "$value"}
            }
        },
        {
            "$sort": {
                "_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": {
                    "$dateToString": {
                        "format": DATETIME_FORMAT,
                        "date": {
                            "$dateFromParts": {
                                "year": "$_id.year",
                                "month": "$_id.month",
                                "day": {"$ifNull": ["$_id.day", 1]},
                                "hour": {"$ifNull": ["$_id.hour", 0]}
                            }
                        }
                    }
                },
                "total_value": 1
            }
        }
    ]

    cursor = db.aggregate(pipeline)
    total_data = await cursor.to_list(length=None)
    dataset = []
    labels = []
    for data_dict in total_data:
        dataset.append(data_dict['total_value'])
        labels.append(data_dict['date'])
    return dataset, labels


def pack_data_to_message(dataset, labels):
    result = json.dumps({'dataset': dataset, 'labels': labels})
    return result
