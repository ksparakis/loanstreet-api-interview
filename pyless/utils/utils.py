import boto3
import json
import datetime
import time
import peewee


def results_to_array(data):
    res = []
    for obj in data:
        for x in obj:
            if isinstance(obj[x], datetime.datetime):
                obj[x] = time.mktime(obj[x].timetuple())
        res.append(obj)
    return res


def rows_to_list_of_dicts(query):
    ret = []
    for row in query:
        ret.append(row)
    return ret

def get_all_vars_from_class(class_):
    """Get all variables in a class object"""
    # print(inspect.getmembers(m.ApplicationCompleted.__module__))
    class_vars = []
    for key, val in class_.__dict__.items():
        if key != "id":
            if isinstance(val, peewee.ForeignKeyAccessor):
                class_vars.append(key)
            elif isinstance(val, peewee.FieldAccessor):
                class_vars.append(key)

    return class_vars
