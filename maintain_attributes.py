#!/usr/bin/env python
from get_attribute import get_one_attribute,get_task_tags,get_task_children
import taskwarrior.taskwarrior as taskwarrior
####################################### attributes values to filter form
def convert_tags_to_filter_form(tags):
    tags_in_filter_form = ''
    if len(tags):
        for tag in tags:
            tags_in_filter_form += f"+{tag} "
    return tags_in_filter_form

def convert_children_to_filter_form(children):
    if len(children) == 0:
        return "child:"
    children_in_filter_form = f'child:{children[0]}'
    children = children[1:]
    if len(children):
        for child in children:
            children_in_filter_form += f",{child}"
    return children_in_filter_form

def convert_attribute_to_filter_form(attribute_name,attribute_value):
    attributes_to_filter_convert_method = {
            "project" : lambda x : f"project:\"{x}\"",
            "tag" : convert_tags_to_filter_form,
            "child" : convert_children_to_filter_form,
            "parents" : lambda x : f"parents:{x}",
            "depends" : lambda x : f"depends:{x}"
            }
    return attributes_to_filter_convert_method[attribute_name](attribute_value)
    
############################# filter form to normal form ######################################
def convert_tag_filter_to_list(tags_in_filter_form):
    tags_and_plussign = tags_in_filter_form.strip().split(' ')
    tags = [ tag_and_plus[1:] for tag_and_plus in tags_and_plussign] 
    if tags[0] == '':
        tags = []
    return tags

def change_child_filter_to_list(child_in_filter_form):
    children = child_in_filter_form.strip().split(',')
    if children[0] == '':
        children = []
    return children

def convert_filter_form_to_attributes(attribute_name,attribute_filter):
    filter_to_attributes_convert_method = {
            "project" : lambda x : x,
            "tag" : convert_tag_filter_to_list,
            "child" : change_child_filter_to_list,
            "parents" : lambda x : x,
            "depends" : lambda x : x
            }
    return filter_to_attributes_convert_method[attribute_name](attribute_filter)

####################################################################
def maintain_attributes(task_uuid, attributes):
    taskwarrior.modify_task_attributes(task_uuid, attributes)

def append_attributes(task_uuid, attribute_name,attribute_value):
    append_attributes_to_original = {
            "project" : lambda uuid,new : new if len(new) else get_one_attribute("project",f"uuid:{uuid}")[0],
            "tag" : lambda uuid,new : get_task_tags(uuid) + [new] if len(new) else get_task_tags(uuid),
            "child" : lambda uuid,new : get_task_children(uuid) + [new] if len(new) else get_task_children(uuid),
            "parents" : lambda uuid,new : new if len(new) else get_one_attribute("parents",f"uuid:{uuid}")[0],
            "depends" : lambda uuid,new : new if len(new) else get_one_attribute("depends",f"uuid:{uuid}")[0]
            }
    new_attributes = append_attributes_to_original[attribute_name](task_uuid,attribute_value)
    maintain_attributes(task_uuid,{attribute_name:new_attributes})

