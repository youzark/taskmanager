#!/usr/bin/env python
import taskwarrior.taskwarrior as taskwarrior

def get_one_attribute(attribute_name,filter):
    wanted_attribute = taskwarrior.query_all_tasks(attribute_name,filter)
    return wanted_attribute

def get_all_tags():
    tag_information = taskwarrior.task("tags",'')
    tag_names_and_count = tag_information.split('\n')[3:-3]
    tag_names = [name_and_count.split(' ')[0] for name_and_count in tag_names_and_count]
    return tag_names

def is_pending(task_uuid):
    status = get_one_attribute("status",f"uuid={task_uuid}")
    if len(status):
        return status[0] == "Pending"

def get_current_working_task_uuid():
    task_uuid = get_one_attribute("uuid","+ACTIVE")
    if len(task_uuid):
        return task_uuid[0]
    else:
        raise Exception("No ACTIVE task")

def get_newly_created_task_uuid():
    return get_one_attribute("uuid","+LATEST")[0]

def get_task_tags(task_uuid):
    return taskwarrior.query_one_task(task_uuid,"tags")

def get_task_children(task_uuid):
    return taskwarrior.query_one_task(task_uuid,"child")

def get_task_project(task_uuid):
    project_name = get_one_attribute("project",f"uuid:{task_uuid}")
    if len(project_name):
        project_name = project_name[0]
    else:
        project_name = ''
    return project_name

# def get_task_tags_in_filter_form(task_uuid):
#     task_tags = get_task_tags(task_uuid)
#     if len(task_tags):
#         tags_in_filter_form = ''
#         for tag in task_tags:
#             tags_in_filter_form = tags_in_filter_form + "+" + tag + " "
#         return tags_in_filter_form
#     else:
#         return ''
