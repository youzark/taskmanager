#!/usr/bin/env python
import taskwarrior.taskwarrior as taskwarrior
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from sub_task import stop,activate_task
from get_attribute import get_all_tags, get_one_attribute
from project_tree import project_tree
from maintain_attributes import maintain_attributes

def parse_project_into_subprojects(projects):
    sub_projects = [ [ sub_projects for sub_projects in projects[i].strip().split(".") ] for i in range(len(projects))]
    return sub_projects

def read_in_project_name():
    projects = taskwarrior.task("_project","").strip().split("\n")
    session = PromptSession()
    completer = WordCompleter(projects)
    project_name = session.prompt("project:",completer=completer)
    return project_name

def create_new_project_and_start():
    stop()
    new_project_name = read_in_project_name()
    if len(new_project_name):
        new_tags = get_all_tags()
        description = f"root task for: {new_project_name}"
        new_task_uuid = taskwarrior.add_new_task(description)
        maintain_attributes(new_task_uuid,{"project":new_project_name,"tag":new_tags})
        activate_task(new_task_uuid)

def activate_project(project_name):
    stop()
    if len(project_name):
        new_task_uuid = get_one_attribute("uuid",f"status:pending project:{project_name}")
        if len(new_task_uuid):
            activate_task(new_task_uuid[0])

def activate_project_from_prompt():
    project_name = read_in_project_name()
    activate_project(project_name)

def readin_subproject_and_prompt_when_has_multiple_choise(root):
    child_nodes = root.children
    if len(child_nodes) == 0:
        return root
    if len(child_nodes) == 1:
        return readin_subproject_and_prompt_when_has_multiple_choise(child_nodes[0])
    else:
        session = PromptSession()
        project_name = root.get_project_prefix()
        subproject_names = [child.project_name for child in child_nodes]
        completer = WordCompleter(subproject_names)
        if len(project_name):
            prompt_content = f"project:{project_name}."
        else:
            prompt_content = "project:"
        subproject_name = session.prompt(prompt_content,completer=completer)
        try:
            selected_project_node = root.get_child_by_name(subproject_name)
        except Exception:
            print("wrong subproject name,try again:")
            subproject_name = session.prompt(prompt_content,completer=completer)
            selected_project_node = root.get_child_by_name(subproject_name)
            return readin_subproject_and_prompt_when_has_multiple_choise(selected_project_node)
        else:
            return readin_subproject_and_prompt_when_has_multiple_choise(selected_project_node)
        

def activate_project_by_subproject():
    root_node = project_tree("root")
    projects = taskwarrior.task("_project",'').strip().split("\n")
    all_subprojects = parse_project_into_subprojects(projects)
    root_node.read_in_subproject_tree(all_subprojects)
    selected_subproject_node = readin_subproject_and_prompt_when_has_multiple_choise(root_node)
    project_name = selected_subproject_node.get_project_prefix()
    activate_project(project_name)

    # all_subproject_choises = { all_subprojects[i][0] for i in range(len(all_subprojects))}
    # session = PromptSession()
    # for iter in range(1,len(all_subprojects)):
    #     completer = WordCompleter(list(all_subproject_choises))
    #     session=PromptSession()
    #     chosed_subproject = session.prompt("subproject",completer=completer)
    #     temp = [ all_subprojects[i] for i in range(len(all_subprojects)) if not all_subprojects[i][iter-1] == chosed_subproject ]
    #     all_subprojects = temp
    #     all_subproject_choises = { all_subprojects[i][iter] for i in range(len(all_subprojects))}
# activate_project_by_subproject()

# def readin_new_tags_in_filter_form():
#     tags = get_all_tags()
#     session = PromptSession()
#     completer = WordCompleter(tags)
#     new_tag = session.prompt("tag:",completer=completer)
#     new_tags_in_filter_form = ""
#     while len(new_tag):
#         new_tags_in_filter_form = new_tags_in_filter_form + f" +{new_tag}"
#         new_tag = session.prompt("    ",completer=completer)
#     return new_tags_in_filter_form
    
