from setuptools import setup,find_packages

setup(
        name = "taskmanager",
        version = "1.0",
        description = "manage task flow and note taking",
        author = "youzark",
        py_modules = ["get_attribute", "sub_task","project","tree","launcher","project_tree","maintain_attributes"],
        install_requires = ['Click'],
        packages = find_packages(),
        entry_points='''
            [console_scripts]
            taskmanager=launcher:cli
        '''
        )
