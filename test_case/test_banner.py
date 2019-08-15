"""
首页Banner页测试
@filename: test_banner.py
@author: hanzhichao
@date: 2018/12/29 16:13
"""
import sys;sys.path.append("..")
import unittest

from ddt import ddt, data, unpack

from utils.common import load_data
from utils.log import logging, log_docstring
from views.h5_view import H5View
from test_case.base_case import BaseCase


class TestBanner(BaseCase):
    """Banner测试"""

    @log_docstring
    def test_watch_banner(self):
        """测试腕表Banner H5页"""
        user = H5View(self.driver)
        user.click_watch_banner()
        self.assertEqual("新年色系腕表甄选推荐", self.driver.title)


if __name__ == "__main__":
    pass
