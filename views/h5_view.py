"""
H5视图
@filename: h5_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class H5View(Common):
    # BANNER = ('id', 'com.secoo:id/banner_image')
    BANNER = ('xpath', '//*[@resource-id="com.secoo:id/tv_desc" and @text="新年色系腕表甄选推荐"]')

    def click_watch_banner(self):
        self.boot_home()
        logging.info("等待点击腕表推荐Banner")
        self.wait_click(*self.BANNER)
        logging.debug("所有上下文： {}".format(self.driver.contexts))
        logging.info("切换上下文到：{}".format("WEBVIEW_com.secoo"))
        self.driver.switch_to.context('WEBVIEW_com.secoo')

    def __del__(self):
        logging.info("切换到上下文: {}".format('NATIVE_APP'))
        self.driver.switch_to.context('NATIVE_APP')


if __name__ == "__main__":
    from utils.device import boot_app
    d = boot_app(device='XY5')
    h = H5View(d)
    h.click_watch_banner()
