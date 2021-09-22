#!/usr/bin/env python
import taskwarrior_double.taskwarrior_double as tsd
import pytest
from taskwarrior_double.helper import is_valid_uuid

def clear_data_file():
    tsd.write_data({})

def create_demo_task_suite():
    """
    + test task1
        - test task2
        - test task3
    """
    uuid1 = tsd.add_new_task("test task1")
    uuid2 = tsd.add_new_task("test task2")
    uuid3 = tsd.add_new_task("test task3")
    tsd.modify_task_attributes(uuid1,{"child":[uuid2,uuid3],"tag":["tag1","tag2"],"project":"test.project"})
    tsd.modify_task_attributes(uuid2,{"parents":uuid1,"tag":["tag1","tag2"],"project":"test.project"})
    tsd.modify_task_attributes(uuid3,{"parents":uuid1,"tag":["tag1","tag2"],"project":"test.project"})
    return (uuid1,uuid2,uuid3)

class TestTaskWarriorDouble:
    """
    add new task
    """
    def test_add_new_task_with_empty_description_raise_ValueError_empty_description(self):
        with pytest.raises(ValueError) as exception_info:
            tsd.add_new_task("")
        assert exception_info.value.args[0] == "empty description"
        clear_data_file()

    def test_add_new_task_with_non_empty_description_do_not_raise_error(self):
        tsd.add_new_task("test description")
        clear_data_file()

    def test_add_new_task_with_non_empty_description_will_return_valid_uuid(self):
        uuid = tsd.add_new_task("test description")
        assert is_valid_uuid(uuid)
        clear_data_file()

    def test_add_new_task_with_non_empty_description_can_be_queried_with_initialize_value(self):
        uuid = tsd.add_new_task("test description")
        assert tsd.query_one_task(uuid,"project") == None
        assert tsd.query_one_task(uuid,"parents") == None
        assert tsd.query_one_task(uuid,"child") == []
        assert tsd.query_one_task(uuid,"tag") == []
        assert tsd.query_one_task(uuid,"depends") == None
        assert tsd.query_one_task(uuid,"status") == "pending"
        clear_data_file()

    """
    modify task attributes
    """
    def test_modify_task_attributes_with_non_exist_uuid_will_raise_KeyError_no_such_task(self):
        with pytest.raises(KeyError) as exception_info:
            tsd.modify_task_attributes("test uuid",{"project":"test project"})
        assert exception_info.value.args[0] == "no such task"
        clear_data_file()

    def test_modify_task_attributes_with_valid_uuid_can_be_queried_correctly(self):
        uuid = tsd.add_new_task("test description")
        tsd.modify_task_attributes(uuid,{"project":"test project","child":["test uuid"]})
        assert tsd.query_one_task(uuid,"project") == "test project"
        assert tsd.query_one_task(uuid,"child") == ["test uuid"]
        clear_data_file()

    """
    query one task
    """
    def test_query_non_exist_task_raise_KeyError_no_such_task(self):
        with pytest.raises(KeyError) as exception_info:
            tsd.query_one_task("test uuid","project")
        assert exception_info.value.args[0] == "no such task"
        clear_data_file()

    def test_query_non_exist_attributes_raise_KeyError_no_such_attribute(self):
        uuid = tsd.add_new_task("test description")
        with pytest.raises(KeyError) as exception_info:
            tsd.query_one_task(uuid,"projects")
        assert exception_info.value.args[0] == "no such attribute"
        clear_data_file()

    def test_query_exist_attribute_return_correct_value(self):
        uuid1,uuid2,uuid3 = create_demo_task_suite()
        assert tsd.query_one_task(uuid1,"child") == [uuid2,uuid3]
        assert tsd.query_one_task(uuid1,"tag") == ["tag1","tag2"]
        assert tsd.query_one_task(uuid1,"project") == "test.project"
        assert tsd.query_one_task(uuid2,"project") == "test.project"
        assert tsd.query_one_task(uuid2,"parents") == uuid1
        clear_data_file()
    """
    query_all_tasks
    """
    def test_query_with_all_tasks_with_empty_filter_attributes_will_return_all_tasks(self):
        all_data = tsd.read_data()
        query_data = tsd.query_all_tasks({})
        assert all_data == query_data
        clear_data_file()


    def test_query_with_non_exist_attribute_or_value_will_return_empty_dictionary(self):
        tsd.add_new_task("test description 1")
        tsd.add_new_task("test description 2")
        tsd.add_new_task("test description 3")
        query_data_non_exist_value = tsd.query_all_tasks({"description":"non_exist"})
        query_data_non_exist_attribute = tsd.query_all_tasks({"non exist":""})
        assert query_data_non_exist_attribute == {}
        assert query_data_non_exist_value == {}
        clear_data_file()

    """
    finish
    """
    def test_finish_non_exist_task_uuid_raise_KeyError(self):
        with pytest.raises(KeyError) as exception_info:
            tsd.finish("test uuid")
        assert exception_info.value.args[0] == "no such task"
        clear_data_file()
    
    def test_finish_task_will_change_status_to_complete(self):
        uuid = tsd.add_new_task("test description")
        tsd.finish(uuid)
        assert tsd.query_one_task(uuid,"status") == "complete"
        clear_data_file()

    """
    start 
    """
    def test_start_non_exist_task_uuid_raise_KeyError(self):
        with pytest.raises(KeyError) as exception_info:
            tsd.start("test uuid")
        assert exception_info.value.args[0] == "no such task"
        clear_data_file()
    
    def test_start_task_will_change_status_to_active(self):
        uuid = tsd.add_new_task("test description")
        tsd.start(uuid)
        assert tsd.query_one_task(uuid,"status") == "active"
        clear_data_file()

    """
    stop
    """
    def test_stop_non_exist_task_uuid_raise_KeyError(self):
        with pytest.raises(KeyError) as exception_info:
            tsd.stop("test uuid")
        assert exception_info.value.args[0] == "no such task"
        clear_data_file()

    def test_stop_task_change_status_to_pending(self):
        uuid = tsd.add_new_task("test description")
        tsd.stop(uuid)
        assert tsd.query_one_task(uuid,"status") == "pending"
        clear_data_file()

    """
    helper function
    """
    def test_has_attributes_return_true_give_empty_attributes(self):
        task_info = {
            "description": "test description",
            "tag" : [],
            "child" : [],
            "parents" : None,
            "depends" : None,
            "project" : None,
            "status" : "pending"
                }
        assert tsd.has_attributes(task_info,{})

    def test_has_attributes_return_False_give_non_exist_attribute(self):
        task_info = {
            "description": "test description",
            "tag" : [],
            "child" : [],
            "parents" : None,
            "depends" : None,
            "project" : None,
            "status" : "pending"
                }
        assert not tsd.has_attributes(task_info,{"test":""})

    def test_has_attributes_return_False_give_non_exist_attribute_value(self):
        task_info = {
            "description": "test description",
            "tag" : [],
            "child" : [],
            "parents" : None,
            "depends" : None,
            "project" : None,
            "status" : "pending"
                }
        assert not tsd.has_attributes(task_info,{"tag":["test_tag"]})

    def test_has_attributes_return_True_give_correct_multiple_attribute_values(self):
        task_info = {
            "description": "test description",
            "tag" : ["test"],
            "child" : ["test"],
            "parents" : "test parent",
            "depends" : None,
            "project" : None,
            "status" : "pending"
                }
        assert tsd.has_attributes(task_info,{"tag":["test"],"child" : ["test"],"depends": None,"status": "pending"})
