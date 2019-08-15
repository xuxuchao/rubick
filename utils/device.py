"""
读取conf/devices.yaml配置
@filename: device.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys; sys.path.append("..")

from appium import webdriver

from utils.common import load_yaml
from utils.config import Config
from utils.log import logging, log_action


class Device(object):

    @classmethod
    def boot_app(cls):
        config = Config()
        run_config = config.get_run_config()

        app = Config.app or run_config.get('app')
        device = Config.device or run_config.get('device')
        hub = Config.hub or run_config.get('hub')

        data = load_yaml('conf', 'devices')
        common = data.get('common') or {}
        if not common or not isinstance(common, dict):
            raise ValueError("app配置错误！")
        app = data.get('apps').get(app)
        if not app or not isinstance(app, dict):
            raise ValueError("app配置错误！")
        device = data.get('devices').get(device)
        if not device or not isinstance(device, dict):
            raise ValueError("device配置错误！")

        hub = data.get('hubs').get(hub)
        if not hub or not isinstance(hub, str):
            raise ValueError("hub配置错误！")

        time_out = run_config.get("implicitly_wait") or 5
        desired_caps = dict(common, **app, **device)
        logging.debug("当前desired_caps: {}".format(desired_caps))
        logging.debug("当前hub: {}".format(hub))

        logging.info("开始启动app")
        dr = webdriver.Remote(hub, desired_caps)
        dr.implicitly_wait(time_out)
        return dr


if __name__ == '__main__':
    # Device.device = 'A9'
    # driver = Device.boot_app()
    logging.info("hello")
