"""
搜索操作
@filename: search_view.py
@author: hanzhichao
@date: 2018/12/27 16:13
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class SearchView(Common):

    HOME_SEARCH = ('id', 'com.secoo:id/home_search_input')
    SEARCH = ('id', 'com.secoo:id/et_title_search')
    RECOMMEND = ['xpath', "//android.widget.TextView[@text='{}']"]
    RESULT_SEARCH = ('id', 'com.secoo:id/tv_title')
    FIRST_GOOD_IMG = ('id', 'com.secoo:id/icon')

    @log_action
    def load_search_page(self):
        self.boot_home()
        logging.info("点击首页搜索框，进入搜索页")
        self.click(*self.HOME_SEARCH)

    @log_action
    def search(self, keyword):
        self.load_search_page()
        logging.info("输入框输入'{}'".format(keyword))
        # import os;os.system("adb shell ime set com.baidu.input/.ImeService")
        # import time; time.sleep(5)
        self.type(*self.SEARCH, text=keyword)
        # time.sleep(5)
        # self.driver.keyevent(66)
        # self.driver.keyevent(84)
        self.RECOMMEND[1] = self.RECOMMEND[1].format(keyword)  # 有时输入了没触发搜索推荐
        logging.info("点击搜索推荐'{}'".format(keyword))
        self.click(*self.RECOMMEND)
        self.click(*self.FIRST_GOOD_IMG)

    @log_action
    def get_search_text(self):
        logging.info("获取搜索结果页搜索框文本")
        return self.find_element(*self.RESULT_SEARCH).get_attribute("text")


if __name__ == "__main__":
    from utils.device import boot_app
    d = boot_app()
    s = SearchView(d)
    s.search("lv")
    logging.info(s.get_search_text())
