#!/usr/bin/env python
import taskwarrior.taskwarrior as taskwarrior
import attribute_formatter as formatter
class attributes:
    def __init__(self,uuid):
        self.uuid = uuid
        self.attributes = {}
        self.filter_form = {}
        self.read_in_attributes(["project", "child" ,"parent","tag","depends"])
        
    def read_in_attributes(self,attriute_names):
        for name in attriute_names:
            value = taskwarrior.query_one_task(self.uuid,name)
            self.attributes[name] = value
            self.attributes[name] = formatter.convert_attribute_to_filter_form(name,value)
