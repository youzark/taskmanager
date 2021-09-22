#!/usr/bin/env python
import attributes.attribute_formatter as af
import pytest

class TestAttributeFormatterAttributeToFilter:
    """
    convert one attribute
    """
    def test_convert_attribute_to_filter_form_empty_attribute_return_empty_filter(self):
        assert af.convert_attribute_to_filter_form("project","") == ""
        assert af.convert_attribute_to_filter_form("tag",[]) == ""
        assert af.convert_attribute_to_filter_form("depends","") == ""
        assert af.convert_attribute_to_filter_form("child",[]) == ""
        assert af.convert_attribute_to_filter_form("parents","") == ""

    def test_convert_attribute_to_filter_form_non_exist_attribute_raise_KeyError_no_such_attribute(self):
        with pytest.raises(KeyError) as error_info:
            af.convert_attribute_to_filter_form("non exist attribute","")
            af.convert_attribute_to_filter_form("non_exist_attribute","")
        assert error_info.value.args[0] == "no such attribute"

    def test_convert_attribute_to_filter_form_return_correct_non_empty_filter(self):
        assert af.convert_attribute_to_filter_form("project","test.project") == "project:test.project"
        assert af.convert_attribute_to_filter_form("tag",['tag1','tag2']) == "+tag1 +tag2"
        assert af.convert_attribute_to_filter_form("depends","test") == "depends:test"
        assert af.convert_attribute_to_filter_form("child",["child1","child2"]) == "child:child1,child2"
        assert af.convert_attribute_to_filter_form("parents","parent") == "parents:parent"

    '''
    convert a set of attributes
    '''
    def test_convert_attributes_to_filter_form_empty_attribute_return_empty_filter(self):
        assert af.convert_attributes_to_filter_form({}) == ""
        assert af.convert_attributes_to_filter_form({"project":"","tag":[]}) == ""

    def test_convert_attributes_to_filter_form_non_exist_attribute_raise_KeyError_no_such_attribute(self):
        with pytest.raises(KeyError) as error_info:
            af.convert_attributes_to_filter_form({"non exist":"no"})
        assert error_info.value.args[0] == "no such attribute"

    def test_convert_attributes_to_filter_form_return_correct_non_empty_filter(self):
        assert af.convert_attributes_to_filter_form({"project":"test.project"}) == "project:test.project"
        assert af.convert_attributes_to_filter_form({"project":"test.project","tag":["tag1","tag2"]}) == "project:test.project +tag1 +tag2"
        assert af.convert_attributes_to_filter_form({"project":"test.project",
            "tag":["tag1","tag2"],
            "child":["child1","child2"]}) == "project:test.project +tag1 +tag2 child:child1,child2"

    '''
    convert command line query result to attribute
    '''
    def test_convert_cmd_query_results_to_attributes_raise_KeyError_with_nonexist_attribute(self):
        with pytest.raises(KeyError) as error_info:
            af.convert_cmd_query_results_to_attributes({"non exist":"test"})
        assert error_info.value.args[0] == "no such attribute"

    def test_convert_cmd_query_results_to_attributes_return_empty_dictionary_with_empty_query_result(self):
        assert af.convert_cmd_query_results_to_attributes({}) == {} 
        assert af.convert_cmd_query_results_to_attributes({"project":""}) == {} 
        assert af.convert_cmd_query_results_to_attributes({"project":"","tag":"","child":""}) == {} 

    def test_convert_cmd_query_results_to_attributes_return_valid_dictionary_with_corresponding_query_result_with_possible_empty_value(self):
        assert af.convert_cmd_query_results_to_attributes({"project":"","tag":"tag1","child":""}) == {"tag":["tag1"]} 
        assert af.convert_cmd_query_results_to_attributes({"project":"test.project",
            "tag":"tag1",
            "child":""}) == {"tag":["tag1"],"project":"test.project"} 
