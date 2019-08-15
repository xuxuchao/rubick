"""
测试用例基础类
@filename: base_case.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")
import unittest
import warnings
from functools import wraps
from urllib3.connectionpool import InsecureRequestWarning

from utils.device import Device
from utils.log import logging


def tag(*tags):
    def _tag(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tags = '\n'.join(tags)
            func.__doc__ += '\n' + _tags
            return func
        return wrapper
    return _tag


class BaseCase(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", InsecureRequestWarning)

        logging.info("{} setUp {}".format("-"*5, "-"*5))
        self.driver = Device.boot_app()

    def tearDown(self):
        logging.info("{} tearDown {}".format("-"*5, "-"*5))
        logging.info("退出")
        self.driver.quit()

        # logging.info("关闭App")
        # self.driver.close_app()


if __name__ == "__main__":
    unittest.main()
