#!/usr/bin/env python
import uuid
import json

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

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
