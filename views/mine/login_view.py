"""
登录操作
@filename: login_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class LoginView(Common):
    MIME_TAB = ('id', "com.secoo:id/tab_item_mine")
    MIME_ICO = ('id', "com.secoo:id/mine_circle_icon")
    NO_LOGIN_NAME = ('id', "com.secoo:id/vm_nologin_name")

    USERNAME_IPT = ('id', "com.secoo:id/input_edit_text")
    PASSWORD_IPT = ('id', "com.secoo:id/input_edit_text")
    # PASSWORD_IPT = ('text', "密码")
    # PASSWORD_IPT = ('xpath', "//TextInputLayout[@resource-id='com.secoo:id/input_text_layout' and @text='密码']/"
    LOGIN_BTN = ('id', "com.secoo:id/app_button_text")

    MIME_SETTINGS = ('id', 'com.secoo:id/mine_setting')
    LOGOUT_BTN = ('id', 'com.secoo:id/setting_logout')
    SURE_BTN = ('id', "com.secoo:id/dialog_button_right")

    @log_action
    def load_mime_page(self):
        self.boot_home()
        logging.info("转到'我的'页面")
        self.wait_click(*self.MIME_TAB)

    @log_action
    def is_login(self):
        if self.try_find_element(*self.MIME_ICO):
            logging.debug("定位到用户头像")
            return True
        else:
            logging.debug("未定位到用户头像")

    @log_action
    def login_action(self, username, password):
        logging.info("登录操作")
        logging.info('用户名: {}'.format(username))
        self.type(*self.USERNAME_IPT, text=username)
        logging.info('密码: {}'.format(password))
        self.find_elements(*self.PASSWORD_IPT)[1].send_keys(password)
        # self.type(*self.PASSWORD_IPT, text=password)
        logging.info('点击登录按钮')
        self.click(*self.LOGIN_BTN)
        logging.info("登录结束")

    @log_action
    def logout_action(self):
        logging.info("============== 退出登录 ===============")
        logging.info("点击设置图标")
        self.click(*self.MIME_SETTINGS)
        logging.info("点击退出登录按钮")
        self.click(*self.LOGOUT_BTN)
        logging.info("点击确认")
        self.click(*self.SURE_BTN)
        logging.info("退出登录结束")

    @log_action
    def login(self, username, password):
        self.load_mime_page()
        # if self.is_login():
        #     logging.info("用户已登录")
        #     return
        logging.debug("点击'登录/注册'链接")
        self.click(*self.NO_LOGIN_NAME)
        self.login_action(username, password)

    @log_action
    def logout(self):
        self.load_mime_page()
        # if not self.is_login():
        #     logging.info("用户未登录")
        #     return
        self.logout_action()


if __name__ == '__main__':
    from utils.device import boot_app
    d = boot_app(device='A9')
    l = LoginView(d)
    l.login("临渊羡鱼", "hanzhichao123")
