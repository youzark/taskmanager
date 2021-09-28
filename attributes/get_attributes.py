#!/usr/bin/env python
import taskwarrior

def get_current_working_task_uuid():
    task_uuid = get_one_attribute("uuid","+ACTIVE")
    if len(task_uuid):
        return task_uuid[0]
    else:
        raise Exception("No ACTIVE task")
