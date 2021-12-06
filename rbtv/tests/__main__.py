from itertools import islice
from typing import Any, Dict, Optional, Sequence, TypedDict, Type
from unittest import TestCase
from inspect import isgenerator

from rbtv import API
from rbtv import types

from typeguard import check_type

class ApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = API()

    def test_all_methods(self):
        methods = [name for name in dir(self.api) if callable(getattr(self.api, name)) and not name.startswith("_")]
        for method in methods:
            func = getattr(self.api, method)
            annotations = func.__annotations__
            if len(annotations) == 1:
                return_type = annotations["return"]
                print(method, return_type)
                result = func()
                if isgenerator(result):
                    result = iter(list(islice(result, 1)))
                try:
                    check_type(result, return_type, argname=method)
                except TypeError:
                    print(result)
                    raise
            else:
                print(f"Skipping {method}")

    def _test_get_bohnen_portraits(self):
        func = self.api.get_bohnen_portraits
        result = func()[0]
        
        try:
            check_type("bohnePortrait", result, getattr(types, "bohnePortrait"))
        except TypeError as e:
            print(func)
            print(result)
            print(e)
            assert False

    def _test_get_blog_posts(self):
        func = self.api.get_blog_posts
        result = list(islice(func(), 1))[0]
        try:
            check_type("blogResponse", result, getattr(types, "blogResponse"))
        except TypeError as e:
            print(func)
            print(result)
            print(e)
            assert False

    def _test_get_shows(self):
        func = self.api.get_shows
        result = list(islice(func(), 1))[0]
        try:
            check_type("mediaShowResponse", result, getattr(types, "mediaShowResponse"))
        except TypeError as e:
            print(func)
            print(result)
            print(e)
            assert False

    def _test_get_featured_shows_preview(self):
        func = self.api.get_featured_shows_preview
        result = func()[0]
        try:
            check_type("mediaShowPreviewResponse", result, getattr(types, "mediaShowPreviewResponse"))
        except TypeError as e:
            print(func)
            print(result)
            print(e)
            assert False


if __name__ == "__main__":
    import unittest

    unittest.main()
