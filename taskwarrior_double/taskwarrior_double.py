#!/usr/bin/env python
import json
import uuid
from taskwarrior_double.helper import *

"""
double for taskwarrior:
    utility:
        1: add new task with description
        2: start a task
        3: finish a task
        4: stop executing
        5: query one attribute for one task
        6: query one attributes for all tasks
        7: modify attributes of a give task
"""


'''
create a new task instance in database with description
return uuid of new task
'''
def add_new_task(description):
    if not bool(len(description)):
        raise ValueError("empty description")
    new_uuid = str(uuid.uuid4())
    attributes = {
            "description": description,
            "tag" : [],
            "child" : [],
            "parents" : None,
            "depends" : None,
            "project" : None,
            "status" : "pending"
            }
    append_data_files(new_uuid,attributes)
    return new_uuid

'''
return specific attribute value of a task
'''
def query_one_task(task_uuid,attribute_name):
    attribute_value = read_attributes(task_uuid,attribute_name)
    return attribute_value

def query_all_tasks(attributes_filter):
    data = read_data()
    query_result = { task_uuid:data[task_uuid] for task_uuid in data if has_attributes(data[task_uuid],attributes_filter)  }
    return query_result

def modify_task_attributes(task_uuid,attributes):
    data = read_data()
    try:
        for attribute_name in attributes:
            data[task_uuid][attribute_name] = attributes[attribute_name]
    except Exception:
        raise KeyError("no such task")
    write_data(data)

def start(task_uuid):
    data = read_data()
    try:
        data[task_uuid]["status"] = "active"
    except Exception:
        raise KeyError("no such task")
    write_data(data)

def stop(task_uuid):
    data = read_data()
    try:
        data[task_uuid]["status"] = "pending"
    except Exception:
        raise KeyError("no such task")
    write_data(data)

def finish(task_uuid):
    data = read_data()
    try:
        data[task_uuid]["status"] = "complete"
    except Exception:
        raise KeyError("no such task")
    write_data(data)

def get_active_task_uuid():
    active_task = query_all_tasks({"status": "active"})
    if len(active_task):
        return list(active_task.keys())[0]
    else:
        raise Exception("no active task")

