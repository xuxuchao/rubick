"""
跳过启动页，关闭广告等常用业务操作
@filename: common_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys;sys.path.append("..")

from views.base_view import BaseView
from utils.log import logging, log_action


class Common(BaseView):
    """常用业务操作"""
    SKIP_TEXT = ('id', 'com.secoo:id/skip_txt')
    HOME_AD_CLOSE = ('id', 'com.secoo:id/global_close')
    HOME_TAB = ('id', 'com.secoo:id/tab_layout')
    PERMISSION_ALLOW_BUTTON = ('id', 'com.android.packageinstaller:id/permission_allow_button')

    @log_action
    def skip_screen(self):
        """跳过启动页"""
        logging.info("尝试在启动页点击'跳过'按钮")
        result = self.try_click(*self.SKIP_TEXT)  # todo change yaml load every time
        logging.info("跳过成功" if result else "没有定位到'跳过'按钮")

    @log_action
    def permission_allow(self):
        """关闭授权对话框"""
        logging.info("尝试在授权对话框点击'总是允许'")
        result = self.try_click(*self.PERMISSION_ALLOW_BUTTON)
        logging.info("授权成功" if result else "没有出现授权对话框")

    @log_action
    def close_home_ads(self):
        """关闭首页广告或升级提示"""
        logging.info("尝试关闭首页广告/升级提示")
        result = self.try_click(*self.HOME_AD_CLOSE)
        logging.info("关闭成功" if result else "广告/升级提示未出现")

    @log_action
    def boot_home(self):
        """启动到首页"""
        logging.info("启动到首页")
        self.permission_allow()
        self.skip_screen()
        self.close_home_ads()

    @log_action
    def back_home(self):
        """返回首页"""
        logging.info("返回首页")
        self.click(*self.HOME_TAB)


if __name__ == '__main__':
    from utils.device import boot_app
    d = boot_app()
    c = Common(d)
    c.skip_screen()
    c.close_home_ads()
    c.screenshot("home")
    d.quit()
