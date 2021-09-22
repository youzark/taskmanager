#!/usr/bin/env python

class project_tree:
    def __init__(self,sub_project_name):
        self.project_name = sub_project_name
        self.parent = None
        self.children = []
        self.depth = 0

    def add_depth_recursively(self):
        if len(self.children):
            self.depth += 1
            for child_node in self.children:
                child_node.add_depth_recursively()

    def add_child(self,sub_project_node):
        self.children.append(sub_project_node)
        sub_project_node.parent = self
        sub_project_node.depth = self.depth + 1;
        sub_project_node.add_depth_recursively()

    def get_project_prefix(self):
        # return nothing of "auxiliary" root node
        if self.parent == None:
            return ''
        else:
            parent_prefix = self.parent.get_project_prefix()
            if len(parent_prefix):
                return  parent_prefix + "." + self.project_name
            else:
                return self.project_name

    def read_in_subproject_tree(self,subprojects):
        length = 0
        for subproject in subprojects:
            length += len(subproject)
        if length:
            subproject_names = { list(subprojects)[i][0] for i in range(len(subprojects))}
            for subproject_name in subproject_names:
                new_subprojects = [ subproject[1:] for subproject in subprojects if subproject[0] == subproject_name ]
                new_node = project_tree(subproject_name)
                self.add_child(new_node)
                new_node.read_in_subproject_tree(new_subprojects)

    def get_child_by_name(self,project_name):
        for child in self.children:
            if child.project_name == project_name:
                return child
        raise Exception("No subproject has given name")


    def print_tree(self):
        if len(self.children):
            print("  "*self.depth,f"+{self.project_name}")
            for child_node in self.children:
                child_node.print_tree()
        else:
            print("  "*self.depth,f"-{self.project_name}")

# tree_node = project_tree("root")
# projects = run("task _project",shell=True,capture_output=True).stdout.decode().strip().split("\n")
# subprojects = parse_project_into_subprojects(projects)
# tree_node.read_in_subproject_tree(parse_project_into_subprojects(projects))
# tree_node.print_tree()
