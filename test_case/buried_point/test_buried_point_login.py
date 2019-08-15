"""
登录埋点测试
@filename: test_buried_point_login.py
@author: hanzhichao
@date: 2019/01/09 17:33
"""
import sys;sys.path.append("../..")
import json
import unittest

from utils.log import logging, log_docstring
from views.mine.login_view import LoginView
from test_case.base_case import BaseCase
from utils.sensors import Sensors
from utils.common import MyThread


class TestBuriedPointLogin(BaseCase):
    """登录埋点测试"""

    @log_docstring
    def test_login_method(self):
        """
        神策登录方法埋点测试
        sensors
        """
        username, password = "18010181267", "hanzhichao123"
        s = Sensors()
        # s = Sensors(headless=False)
        logging.info("登录神策并监控数据")
        s.login("houyanan@secoo.com", "houyanan")
        s.start_check("Login", '130810251181')
        logging.info("使用密码进行登录")
        user = LoginView(self.driver)
        user.login(username, password)
        logging.info("按Home键")
        self.driver.keyevent(3)
        data = s.get_data()
        logging.info(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
        self.assertEqual("密码登录", data.get("properties").get("login_method"))


if __name__ == '__main__':
    unittest.main()
