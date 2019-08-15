"""
登录测试
@filename: test_buried_point_login.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")
import unittest

from ddt import ddt

from utils.log import logging, log_docstring
from views.mine.login_view import LoginView
from test_case.base_case import BaseCase


@ddt
class TestLogin(BaseCase):
    """登录测试"""
    # device = 'SauceLabA'
    # hub = 'sauce_lab_eu'

    @log_docstring
    def test_login_normal(self):
        """
        正常登录测试
        smoke
        """
        username, password = "18010181267", "hanzhichao123"
        logging.info("正常登录测试，用户名：{}, 密码: {}".format(username, password))
        user = LoginView(self.driver)
        user.login(username, password)
        self.assertTrue(user.is_login())

    # @data(*load_data('login'))
    # @unpack
    # def test_login_normal_with_ddt(self, username, password):
    #     """正常登录测试"""
    #     logging.info("正常登录测试，用户名：{}, 密码: {}".format(username, password))
    #     user = LoginView(self.driver)
    #     user.login(username, password)
    #     self.assertTrue(user.is_login())

    @log_docstring
    def test_login_negative(self):
        """异常登录测试"""
        user = LoginView(self.driver)
        user.login("Abc", '123')
        user.screenshot('login')
        self.assertIsNotNone(user.wait_toast("账号与密码不匹配"))


if __name__ == '__main__':
    unittest.main()
