#!/usr/bin/env python
import click
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from sub_task import add_and_acrivate_new_subtask,finish,stop
from project import create_new_project_and_start,activate_project_from_prompt,activate_project_by_subproject


functionalities = {
        "start":activate_project_by_subproject,
        "stop":stop,
        "finish":finish,
        "new subtask":add_and_acrivate_new_subtask,
        "new project":create_new_project_and_start,
        }

@click.command()
def cli():
    functions = list(functionalities.keys())
    function_completer = WordCompleter(functions)
    session = PromptSession()
    selected_function = session.prompt("function:",completer=function_completer)
    if len(selected_function):
        functionalities[selected_function]()
