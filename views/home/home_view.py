"""
首页操作
@filename: home_view.py
@author: hanzhichao
@date: 2019/01/07 15:45
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class HomeView(Common):
    HOME = ('id', 'com.secoo:id/tab_layout')
    DISCOVERY = ('id', 'com.secoo:id/tab_item_brand')
    CATEGORY = ('id', 'com.secoo:id/tab_item_category')
    CART = ('id', 'com.secoo:id/tab_item_cart')
    MIME = ('id', 'com.secoo:id/tab_item_mine')

    def click_discovery(self):
        logging.info("点击'发现'")
        self.click(*self.DISCOVERY)

    def click_category(self):
        logging.info("点击'分类'")
        self.click(*self.CATEGORY)

    def click_cart(self):
        logging.info("点击'购物袋'")
        self.click(*self.CART)

    def click_mime(self):
        logging.info("点击'我的'")
        self.click(*self.MIME)


if __name__ == "__main__":
    pass
