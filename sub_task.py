#!/usr/bin/env python
from maintain_attributes import maintain_attributes
from get_attribute import get_current_working_task_uuid, get_task_project, get_task_tags
from prompt_toolkit import PromptSession
import taskwarrior.taskwarrior as taskwarrior
import tree
    
def activate_task(task_uuid):
    stop()
    task_node = tree.task_node(task_uuid)
    pending_leaves = task_node.get_pending_leaf_tasks()
    print(pending_leaves)
    if len(pending_leaves):
        taskwarrior.start(pending_leaves[0].uuid)
    else:
        taskwarrior.start(task_uuid)

def stop():
    try:
        curent_task_uuid = get_current_working_task_uuid()
    except Exception:
        pass
    else:
        if curent_task_uuid:
            taskwarrior.stop(curent_task_uuid)

def finish():
    curent_task_uuid = get_current_working_task_uuid()
    if len(curent_task_uuid):
        taskwarrior.finish(curent_task_uuid)
        parent_uuid = taskwarrior.query_one_task(curent_task_uuid,"parents")
        if len(parent_uuid):
            activate_task(parent_uuid[0])

def add_subtask(description):
    new_task_uuid = taskwarrior.add_new_task(description)
    print(new_task_uuid,flush=True)
    parent_task_uuid = get_current_working_task_uuid()
    project_name = get_task_project(parent_task_uuid)
    tags = get_task_tags(parent_task_uuid)
    maintain_attributes(new_task_uuid,{"project":project_name, "tag":tags, "parents":parent_task_uuid})
    maintain_attributes(parent_task_uuid,{"child":new_task_uuid,"depends":new_task_uuid})
    return new_task_uuid

def add_and_acrivate_new_subtask():
    session = PromptSession()
    description = session.prompt("Description:")
    new_task_uuid = add_subtask(description)
    activate_task(new_task_uuid)

# def add_new_task(description,parent_task_uuid):
#     # get child task attributes:
#     project_name = get_task_project(parent_task_uuid)
#     tags = get_task_tags(parent_task_uuid)
#     new_task_uuid = taskwarrior.add(description)
#     maintain_attributes(new_task_uuid,{"project":project_name, "tag":tags})
#     parent_node = tree.task_node(parent_task_uuid)
#     child_node = tree.task_node(new_task_uuid)
#     parent_node.maitain_tree_when_add_sub_task(child_node)
#     # if len(project_name):
#     #     project_filter_form = "project:"+project_name[0]
#     # else:
#     #     project_filter_form = ''
#     # tags_filter_form = get_task_tags_in_filter_form(parent_task_uuid)
#     # add new task(child task):
#     # command_add_new_task = f"task add {project_filter_form} {tags_filter_form} {description}"
#     # run(command_add_new_task,shell=True,capture_output=True)
#     # new_task_uuid = get_one_attribute("uuid","+LATEST")[0]
#     # maintain tree structure:
#     return child_node

# def add_sub_task(description,attributes):
#     new_task_uuid = taskwarrior.add(description)
#     maintain_attributes(new_task_uuid,attributes)
#     return new_task_uuid

