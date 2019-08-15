"""
搜索测试
@filename: search_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")
import unittest

from ddt import ddt

from utils.log import logging
from views.search.search_view import SearchView
from test_case.base_case import BaseCase


@ddt
class TestSearch(BaseCase):
    """搜索测试"""

    def test_search_normal(self):
        """正常搜索测试"""
        keyword = 'lv'
        logging.info("正常搜索测试，关键词：{}".format(keyword))
        user = SearchView(self.driver)
        user.search(keyword)
        self.assertEqual(keyword, user.get_search_text())

    # @data(*load_data('search'))
    # def test_search_with_ddt(self, keyword):
    #     """正常搜索测试"""
    #     logging.info("正常搜索测试，关键词：{}".format(keyword))
    #     user = SearchView(self.driver)
    #     user.search(keyword)
    #     self.assertEqual(keyword, user.get_search_text())


if __name__ == '__main__':
    unittest.main()
