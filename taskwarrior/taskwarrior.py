#!/usr/bin/env python
from attributes.attribute_formatter import convert_attributes_to_filter_form
from maintain_attributes import convert_attribute_to_filter_form
from subprocess import run
from matadata.matadata import matadata


def task(command,filter,config = ''):
    return run(f"task {config} {filter} {command}",shell=True,capture_output=True).stdout.decode()

###########################################################################
# description: 	add task with given description,return the new uuid
###########################################################################
def add_new_task(description):
    run(f"task add {description}",shell=True,capture_output=True).stdout.decode()
    uuid = query_all_tasks("uuid","+LATEST")[0]
    data = matadata(uuid)
    data.init_matadata_file()
    return uuid
    
###########################################################################
# description: 	modify uuid with given filter(attribute should be given in filter form)
###########################################################################
def modify_task_attributes(task_uuid,attributes):
    filter = ''
    for attribute_name in attributes:
        filter += convert_attribute_to_filter_form(attribute_name,attributes[attribute_name])
    run(f"task {task_uuid} modify {filter}",shell=True,capture_output=True)

###########################################################################
# description: 	start task with given uuid
###########################################################################
def start(task_uuid):
    data = matadata(task_uuid)
    data.workflow_instance_start()
    run(f"task start {task_uuid}",shell=True,capture_output=True)

def stop(uuid):
    data = matadata(uuid)
    data.workflow_instance_end()
    run(f"task stop {uuid}",shell=True,capture_output=True)

def finish(uuid):
    data = matadata(uuid)
    data.workflow_instance_end()
    run(f"task done {uuid}",shell=True,capture_output=True)

def query_one_task(task_uuid,attribute_name):
    attribute = run(f"task _get {task_uuid}.{attribute_name}",shell=True,capture_output=True).stdout.decode().strip()
    if len(attribute):
        attributes = attribute.split(",")
    else:
        attributes = []
    return(attributes)

def query_all_tasks(columns,filter):
    colunm_config = f"rc.report.temp.columns:{columns}"
    filter_config = f"rc.report.temp.filter:{filter}"
    query_command = f"task {colunm_config} {filter_config} temp"
    query_result = run(query_command,shell=True,capture_output=True).stdout.decode()
    attribute = query_result.split("\n")[3:-3] # get ride of useless information
    attributes = [ attri.strip() for attri in attribute ]
    return attributes
