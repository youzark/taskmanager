#!/usr/bin/env python
import json
import time

class matadata:
    def __init__(self,task_uuid):
        self.uuid = task_uuid
        self.path = f"/home/hyx/data/taskmanager/{task_uuid}.json"

    def load_data(self):
        try:
            with open(self.path,"r") as f:
                data = json.load(f)
        except Exception:
            return {} 
        else:
            return data

    def write_data(self,data):
        with open(self.path,"w") as f:
            json.dump(data,f,indent=2)
        

    def init_matadata_file(self):
        data = {
                "workflow" : [],
                "note" : [],
                "reference": []
                }
        print(data)
        self.write_data(data)

    def add_workflow_instance(self,workflow_instance):
        data = self.load_data()
        try:
            data["workflow"].append(workflow_instance)
        except Exception:
            self.init_matadata_file()
            data = self.load_data()
            data["workflow"].append(workflow_instance)
        self.write_data(data)

    def workflow_instance_start(self):
        data = self.load_data()
        time_stamp = time.time()
        workflow_instance = {
                "start" : time_stamp
                }
        try:
            data["workflow"].append(workflow_instance)
        except Exception:
            self.init_matadata_file()
            data = self.load_data()
            data["workflow"].append(workflow_instance)
        self.write_data(data)

    def workflow_instance_end(self):
        data = self.load_data()
        time_stamp = time.time()
        if len(data["workflow"]):
            data["workflow"][-1]["end"] = time_stamp
        self.write_data(data)

    def add_note(self,note_path):
        data = self.load_data()
        data["note"].append(note_path)
        self.write_data(data)

    def add_reference(self,reference_path):
        data = self.load_data()
        data["reference"].append(reference_path)
        self.write_data(data)

    def get_workflows(self):
        data = self.load_data()
        return data["workflow"]

    def get_task_duration(self):
        workflow = self.get_workflows()
        duration = 0
        for instance in workflow:
            duration += instance["end"] - instance["start"]
        return duration
    
    def get_notes(self):
        data = self.load_data()
        return data["note"]

    def get_references(self):
        data = self.load_data()
        return data["reference"]
