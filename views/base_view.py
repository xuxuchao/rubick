"""
封装元素/页面基本操作
@filename: base_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys; sys.path.append("..")

import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from utils.log import logging, log_action
from utils.config import Config, PROJECT_ROOT


class BaseView(object):
    """页面基本操作"""
    def __init__(self, driver):
        self.driver = driver
        self.config = Config()
        run_config = self.config.get_run_config()
        self.TIME_OUT = run_config.get("webdriver_wait") or 20
        # time.sleep(1)

    # 元素定位 -------------------------------------------------------------------
    @log_action
    def find_text(self, text):
        """使用text定位元素"""
        text = text.strip()
        if not text:
            raise ValueError
        return self.driver.find_element_by_android_uiautomator('new UiSelector().text("{}")'.format(text))

    @log_action
    def find_id(self, resource_id):
        """使用id定位元素"""
        if not resource_id:
            raise ValueError("resource_id参数不能为空")
        return self.driver.find_element_by_id(resource_id)

    @log_action
    def find_element(self, *loc):
        """定位元素，支持id,class_name, xpath, text, msg"""
        if len(loc) != 2:
            raise ValueError("参数定位器长度不为2")
        if loc[0].lower() in ('id', 'class_name', 'xpath'):
            return self.driver.find_element(*loc)
        elif loc[0].lower() == 'text':
            return self.find_text(loc[1])
        elif loc[0].lower() == 'msg':
            return self.wait_toast(loc[1])

        else:
            raise ValueError("不支持该种定位方式")

    @log_action
    def find(self, *loc):
        """定位元素，找不到则截图，并报错"""
        try:
            return self.find_element(*loc)
        except NoSuchElementException:
            time.sleep(1)  # todo check
            self.screenshot('NotFound_{}'.format('_'.join(loc)))
            logging.error("定位元素: {} 失败".format(loc))
            raise

    @log_action
    def try_find_element(self, *args):
        """尝试定位元素，找不到不报错"""
        try:
            return self.find_element(*args)
        except NoSuchElementException:
            logging.debug("元素: {} 未被定位到".format(args))

    @log_action
    def find_elements(self, *loc):
        """定位一组元素，只支持id, class name, xpath"""
        if len(loc) !=2:
            raise ValueError
        return self.driver.find_elements(*loc)
    
    @log_action
    def wait_element(self, *loc):
        """等待并检测元素，定位不到元素报超时错误"""
        try:
            wait = WebDriverWait(self.driver, self.TIME_OUT)
            return wait.until(lambda _: self.find_element(*loc))
        except TimeoutException:
            self.screenshot('NotFound_{}'.format('_'.join(loc)))
            logging.error("元素 {} 超时未定位到".format(loc))
            raise

    @log_action
    def wait_text(self, text):
        """等待并检测指定text元素，定位不到报超时错误"""
        try:
            wait = WebDriverWait(self.driver, self.TIME_OUT)
            return wait.until(lambda _: self.find_text(text))
        except TimeoutException:
            self.screenshot('NotFound_text_{}'.format(text))
            logging.error("文本 {} 超时未定位到".format(text))
            raise

    @log_action
    def wait_toast(self, msg):
        """等待并检测toast消息，定位不到报超时错误"""
        try:
            return self.wait_element('xpath', '//*[@text="{}"]'.format(msg))
        except TimeoutException:
            self.screenshot('NotFound_msg_{}'.format(msg))
            logging.error("提示消息 {} 超时未定位到".format(msg))
            raise

    # 元素操作 -------------------------------------------------------------------
    @log_action
    def click_text(self, *args):
        """点击指定文本元素"""
        logging.debug("点击文本: {}".format(args))
        self.find_text(*args).click()

    @log_action
    def click_id(self, *args):
        """点击指定resource_id元素"""
        logging.debug("点击指定id: {} 元素".format(args))
        self.find_id(*args).click()

    @log_action
    def click(self, *args):
        """点击元素，支持id,class name,xpath, text, msg, 点击不到则截图并报错"""
        logging.debug("点击: {}".format(args))
        self.find(*args).click()

    @log_action
    def wait_click(self, *args):
        """等待并点击元素，定位不到报超时错误"""
        logging.debug("等待点击: {}".format(args))
        self.wait_element(*args).click()

    @log_action
    def try_click_text(self, text):
        """尝试点击指定文本，定位不到不报错"""
        logging.debug("尝试点击文本: {}".format(text))
        try:
            self.find_text(text).click()
            return True
        except NoSuchElementException:
            logging.debug("文本: {} 未被定位到".format(text))

    @log_action
    def try_click_id(self, resource_id):
        """尝试点击指定resource_id元素，定位不到不报错"""
        logging.debug("尝试点击指定id: {} 元素".format(resource_id))
        try:
            self.find_id(resource_id).click()
            return True
        except NoSuchElementException:
            logging.debug("指定id: {} 元素 未被定位到".format(resource_id))

    @log_action
    def try_click(self, *args):
        """尝试点击指定元素，定位不到不报错"""
        logging.debug("尝试点击: {}".format(args))
        try:
            self.find_element(*args).click()
            return True
        except NoSuchElementException:
            logging.debug("元素: {} 未被定位到".format(args))

    @log_action
    def type(self, *args, text=''):
        """输入，args为元素定位符，支持id，class name, xpath, text, msg"""
        logging.debug("元素: {} 输入: {}".format(args, text))
        text = text.strip()
        if not text:
            logging.warning("type() text参数为空!")
        input = self.find_element(*args)
        input.clear()
        input.send_keys(text)

    @log_action
    def type_and_enter(self, *args, text=''):
        """输入并按回车键"""
        self.type(*args, text=text)
        logging.debug("按回车键")
        self.driver.keyevent(66)

    @log_action
    def type_and_search(self, *args, text=''):
        """输入并按搜索键"""
        self.type(*args, text=text)
        logging.debug("按搜索键")
        self.driver.keyevent(84)

    # page action --------------------------------------------------------------
    @log_action
    def long_touch(self):  # todo complete
        """长按"""
        pass

    @log_action
    def get_screen_size(self):
        """获取屏幕尺寸"""
        size = self.driver.get_window_size()
        return (size['width'], size['height'])

    @log_action
    def swip_left(self, from_top=0.5):
        """左划，from_top默认为距离顶部0.5个屏幕(屏幕中间)"""
        if not isinstance(from_top, int) and not isinstance(from_top, float):
            raise ValueError("from_top参数不为数字")
        logging.debug("左滑")
        l = self.get_screen_size()
        y1 = int(l[1]*from_top)
        x1 = int(l[0]*0.95)
        x2 = int(l[0]*0.25)
        self.driver.swipe(x1, y1, x2, y1, 1000)

    @log_action
    def swip_right(self, from_top=0.5):
        """右划，from_top默认为距离顶部0.5个屏幕(屏幕中间)"""
        if not isinstance(from_top, int) and not isinstance(from_top, float):
            raise ValueError("from_top参数不为数字")
        logging.debug("右滑")
        l = self.get_screen_size()
        y1 = int(l[1]*from_top)
        x1 = int(l[0]*0.25)
        x2 = int(l[0]*0.95)
        self.driver.swipe(x1, y1, x2, y1, 1000)

    @log_action
    def swip_up(self, from_left=0.5):
        """上划，from_left默认为距离左侧0.5个屏幕(屏幕中间)"""
        if not isinstance(from_left, int) and not isinstance(from_left, float):
            raise ValueError("from_left参数不为数字")
        logging.debug("上滑")
        l = self.get_screen_size()
        x1 = int(l[1]*from_left)
        y1 = int(l[0]*0.95)
        y2 = int(l[0]*0.25)
        self.driver.swipe(x1, y1, x1, y2, 1000)

    @log_action
    def swip_down(self, from_left=0.5):
        """下划，from_left默认为距离左侧0.5个屏幕(屏幕中间)"""
        if not isinstance(from_left, int) and not isinstance(from_left, float):
            raise ValueError("from_left参数不为数字")
        logging.debug("下滑")
        l = self.get_screen_size()
        x1 = int(l[1]*from_left)
        y1 = int(l[0]*0.25)
        y2 = int(l[0]*0.95)
        self.driver.swipe(x1, y1, x1, y2, 1000)

    @log_action
    def screenshot(self, module):
        snapshot_dir = Config.task_dir or os.path.join(PROJECT_ROOT, 'report/snapshot')
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        image_file = os.path.join(snapshot_dir, "{}_{}.png".format(module, now))
        logging.debug("获取 {} 模块屏幕截图".format(module))
        logging.debug("截图文件路径: {}".format(image_file))
        self.driver.get_screenshot_as_file(image_file)

    # 按键 ---------------------------------------------------------------------
    @log_action
    def back(self):
        """按返回键"""
        self.driver.keyevent(4)


if __name__ == '__main__':
    from utils.device import Device
    driver = Device.boot_app()
    e = BaseView(driver)
    e.find_text("奢侈品")
    e.find_element("id", "com.secoo:id/home_search_input")
    e.find_yaml_element('home', 'common', 'nIcoMsg').click()
    # e.click("id", "com.secoo:id/home_search_input")
    from time import sleep
    sleep(5)
    driver.quit()
