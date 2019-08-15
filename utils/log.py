"""
日志配置及装饰器
@filename: log.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")

import os
import logging as l
import time
from functools import wraps

from utils.config import PROJECT_ROOT, Config


class Log(object):
    logger = l.getLogger()

    @classmethod
    def config_logger(cls):
        log_config = Config.get_log_config()
        log_dir = log_config.get('log_dir') or 'log'
        log_level = log_config.get('log_level') or 'debug'
        log_level = eval("l.{}".format(log_level.upper()))

        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log_dir = os.path.join(PROJECT_ROOT, log_dir)

        # 总日志，按天分割
        total_log_file = os.path.join(log_dir, '{}.log'.format(date))
        # 单次运行日志
        task_log_dir = Config.task_dir or log_dir
        print(Config.task_dir)
        task_log_file = os.path.join(task_log_dir, 'log.log')

        cls.logger.setLevel(log_level)

        fh1 = l.FileHandler(total_log_file, mode='a', encoding='utf-8')
        fh1.setLevel(l.DEBUG)

        fh2 = l.FileHandler(task_log_file, mode='a', encoding='utf-8')
        fh2.setLevel(log_level)

        ch = l.StreamHandler()
        ch.setLevel(log_level)

        formatter = l.Formatter("%(asctime)s %(filename)s[%(lineno)d] %(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S")
        fh1.setFormatter(formatter)
        fh2.setFormatter(formatter)
        ch.setFormatter(formatter)

        cls.logger.addHandler(fh1)
        cls.logger.addHandler(fh2)
        cls.logger.addHandler(ch)

    @classmethod
    def get_logger(cls):
        cls.config_logger()
        return cls.logger


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        back = func(*args, **kwargs)
        exec_time = time.time()-t0 
        logging.debug("调用: {}() 执行时间: {}s".format(func.__name__,exec_time))
        return back
    return wrapper


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("调用: {}() 参数: {}".format(func.__name__, args or kwargs))
        return func(*args, **kwargs)
    return wrapper


def log_docstring(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        doc = func.__doc__
        doc = doc and doc.strip().split("\n")[0].strip() or func.__name__
        logging.info("------ {} ------".format(doc))
        return func(*args, **kwargs)
    return wrapper


logging = Log.get_logger()

if __name__ == '__main__':
    logging = Log.get_logger()
    logging.info("hello 中文")

    @log_action
    def func(a, b):
        print("...")

    @log_time
    def func2(a, b):
        print("...")

    @log_docstring
    def func3(a, b):
        """hello"""
        print("i run")

    func(a=1, b=2)
    func2(1, 2)
    func3(1,2)
