#!/usr/bin/env python
import attributes.attribute_formatter as af
import pytest

class TestAttributeFormatterAttributeToFilter:
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

