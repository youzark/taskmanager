#!/usr/bin/env python

def convert_attributes_to_filter_form(attributes):
    filter = ''
    for attribute_name in attributes:
        filter = filter + convert_attribute_to_filter_form(attribute_name,attributes[attribute_name]) + " "
    return filter.strip()

def convert_attribute_to_filter_form(attribute_name,attribute_value):
    attributes_to_filter_convert_method = {
            "project" : lambda x : f"project:{x}" if len(x) else "",
            "tag" : convert_tags_to_filter_form,
            "child" : convert_children_to_filter_form,
            "parents" : lambda x : f"parents:{x}" if len(x) else "",
            "depends" : lambda x : f"depends:{x}" if len(x) else ""
            }
    try:
        return attributes_to_filter_convert_method[attribute_name](attribute_value).strip()
    except KeyError:
        raise KeyError("no such attribute")

def convert_tags_to_filter_form(tags):
    tags_in_filter_form = ''
    if len(tags):
        for tag in tags:
            tags_in_filter_form += f"+{tag} "
    return tags_in_filter_form

def convert_children_to_filter_form(children):
    if len(children) == 0:
        return ""
    children_in_filter_form = f'child:{children[0]}'
    children = children[1:]
    if len(children):
        for child in children:
            children_in_filter_form += f",{child}"
    return children_in_filter_form

############################# query result to normal form(attribute) ######################################
def convert_cmd_query_results_to_attributes(attribute_query_result):
    filter_to_attributes_convert_method = {
            "project" : lambda x : x,
            "tag" : convert_tag_query_to_list,
            "child" : change_child_filter_to_list,
            "parents" : lambda x : x,
            "depends" : lambda x : x
            }
    try:
        attributes = { attribute_name:filter_to_attributes_convert_method[attribute_name](attribute_query_result[attribute_name]) 
                    for attribute_name in attribute_query_result 
                    if len(attribute_query_result[attribute_name])  }
        return attributes
    except KeyError:
        raise KeyError("no such attribute")

def convert_tag_query_to_list(tags_in_filter_form):
    tags_and_plussign = tags_in_filter_form.strip().split(' ')
    tags = [ tag_and_plus for tag_and_plus in tags_and_plussign] 
    if tags[0] == '':
        tags = []
    return tags

def change_child_filter_to_list(child_in_filter_form):
    children = child_in_filter_form.strip().split(',')
    if children[0] == '':
        children = []
    return children
