#!/usr/bin/env python
import get_attribute
from maintain_attributes import append_attributes


class task_node:
    ###########################################################################
    # description: 	recursively init the whold subtree
    # parameter: 	uuid root of the tree (can be a subtree root)
    ###########################################################################
    def __init__(self,uuid):
        self.uuid = uuid
        self.child = []
        self.parent = None
        self.depth = 0
        # read in the subtree
        child_string = get_attribute.get_one_attribute("child",f"uuid:{self.uuid}")
        if len(child_string):
            child_uuid_list = child_string[0].strip().split(',')
            print(self.uuid,child_uuid_list,child_string)
            for child_uuid in child_uuid_list:
                child_node = task_node(child_uuid)
                self.add_child(child_node)

    def add_depth_recursive(self):
        for child_node in self.child:
            child_node.depth += 1
            child_node.add_depth_recursive()

    ###########################################################################
    # description: 	only add existing subtask to this data structure
    # parameter: 	
    ###########################################################################
    def add_child(self,child_node):
        self.child.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1
        child_node.add_depth_recursive()

    ###########################################################################
    # description: 	read from task warrior to construct a tree of task node
    # parameter: 	
    ###########################################################################
    # def read_in_task_tree(self):
    #     child_string_list = get_attribute.get_one_attribute("child",f"uuid={self.uuid}")
    #     if child_string_list:
    #         child_string = child_string_list[0]
    #         child_uuid_list = child_string.strip().split(",")
    #         for child_uuid in child_uuid_list:
    #             child_node = task_node(child_uuid)
    #             self.add_child(child_node)
    #             child_node.read_in_task_tree()
        
    ###########################################################################
    # description: 	maintain task "child "and "parents" attributes and this data structure.
    # parameter: 	
    ###########################################################################
    def maitain_tree_when_add_sub_task(self,child_node):
        append_attributes(self.uuid,"child",child_node.uuid)
        append_attributes(child_node.uuid,"parents",self.uuid)
        self.add_child(child_node)

    def get_pending_leaf_tasks(self):
        pending_leaves = []
        for child in self.child:
            if get_attribute.is_pending(child.uuid):
                child_pending_leaves = child.get_pending_leaf_tasks()
                if not bool(len(child_pending_leaves)):
                    pending_leaves.append(child)
                else:
                    pending_leaves += child_pending_leaves
        return pending_leaves
            
    def print_node_attribute_in_tree(self,attributes=[]):
        for attribute in attributes:
            attribute_value = get_attribute.get_one_attribute(f"{attribute}",f"uuid:{self.uuid}")
            print("    "*self.depth,f' |{attribute}:{attribute_value}')


    def print_task_tree(self,attributes=[]):
        child_nodes = self.child
        if child_nodes:
            print("  "*self.depth,'+',self.uuid)
            self.print_node_attribute_in_tree(attributes)
            for child_node in child_nodes:
                child_node.print_task_tree(attributes)
        else:
            print("  "*self.depth,'- ',self.uuid)
            self.print_node_attribute_in_tree(attributes)


# root_task = task_node(get_attribute.get_one_attribute("uuid","id:1")[0])
# root_task.print_task_tree(["description","status","child","parents"])
# pending_uuid = root_task.get_pending_leaf_tasks()[0].uuid
# pending_task_node = task_node(pending_uuid)
# pending_task_node.print_task_tree()
# print(pending_task_node.get_pending_leaf_tasks())
