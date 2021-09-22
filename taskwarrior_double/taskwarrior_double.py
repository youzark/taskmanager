#!/usr/bin/env python
import json
import uuid

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
###########################################################################
# description: 	   change state
###########################################################################

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

"""
helper functions
"""
def has_attributes(task_info, attributes):
    for attribute_name in attributes:
        try:
            if task_info[attribute_name] != attributes[attribute_name]:
                return False
        except KeyError:
            return False
    return True

def write_data(data):
    file_name = "data.json"
    with open(file_name,"w") as f:
        json.dump(data,f,indent = 4)
    
def read_attributes(task_uuid,attribute_name):
    data = read_data()
    try:
        task_info = data[task_uuid]
    except Exception:
        raise KeyError("no such task")
    try:
        attribute_value = task_info[attribute_name]
    except Exception:
        raise KeyError("no such attribute")
    return attribute_value

def read_data():
    file_name = "data.json"
    with open(file_name,"r") as f:
        data = json.load(f)
        return data

def append_data_files(new_uuid,attributes):
    data = read_data()
    data[new_uuid] = attributes
    write_data(data)

