"""
读取conf/config.yaml配置
@filename: config.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")
import os
import time

import yaml

# 项目绝对路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    conf_dir = 'conf'
    conf_file = 'config'
    app = ''
    device = ''
    hub = ''
    task_dir = ''

    # now = time.strftime('%Y%m%d_%H%M%S', time.localtime())

    # 为每次的报告建立独立的文件夹
    # task_dir = os.path.join(PROJECT_ROOT, 'report', "task_{}".format(now))   # todo config
    # if not os.path.exists(task_dir):
    #     os.makedirs(task_dir)
    # report_file = os.path.join(task_dir, 'report.html')

    yaml_file = "{}.yaml".format(os.path.join(PROJECT_ROOT, conf_dir, conf_file))
    with open(yaml_file, encoding='utf-8') as f:
        data = yaml.load(f)

    @classmethod
    def get(cls, section):
        return cls.get(section)
    
    @classmethod
    def get_log_config(cls, section='log'):
        log_config = cls.data.get(section)
        return log_config

    @classmethod
    def get_run_config(cls, section='run'):
        run_config = cls.data.get(section)
        return run_config
    
    @classmethod
    def get_report_config(cls, section='report'):
        report_config = cls.data.get(section)
        return report_config
    
    @classmethod
    def get_snapshot_config(cls, section='snapshot'):
        snapshot_config = cls.data.get(section)
        return snapshot_config
    
    @classmethod
    def get_email_config(cls, section='email'):
        email_config = cls.data.get(section)
        return email_config


if __name__ == "__main__":
    c = Config
    print(c.get_run_config())
    c.get_email_config()
    c.get_report_config()
    c.get_log_config()





