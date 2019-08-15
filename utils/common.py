"""
常用方法
@filename: conmmon.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")
import os
import yaml
import threading

from utils.log import logging, log_action
from utils.config import PROJECT_ROOT


@log_action
def load_yaml(*args):
    try:
        yaml_file = "{}.yaml".format(os.path.join(PROJECT_ROOT, *args))
        with open(yaml_file, encoding='utf-8') as f:
            data = yaml.load(f)
            logging.debug("Yaml文件数据: {}".format(data))
            return data
    except IOError:
        logging.error("打开 {} 失败!".format(yaml_file))
        logging.exception(sys.exc_info())


def load_data(data_file):
    data = load_yaml('data', data_file)
    return data


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


if __name__ == '__main__':
    print(load_yaml('conf', 'config'))


