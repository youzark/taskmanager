#!/usr/bin/env python
import re

'''
command format:
    task filter command modifications [miscellaneous]

filter(modifications):
    +word +word
    project:project_name
    child:child1,child2
    parents:parents_name
    depends:uuid
    status:pending
    description

command:
    add
    modify
    start
    stop
    done
    _get
'''
command = ["add","modify","start","stop","done","_get"]
filter_recognizer = {
        }

def parse_command(command):

