"""
商品详情操作
@filename: goods_detail_view.py
@author: hanzhichao
@date: 2019/01/07 11:13
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class GoodsDetailView(Common):
    COLLECTION = ('id', 'com.secoo:id/ll_collection')
    CUSTOMER_SERVICE = ('id', 'com.secoo:id/ll_customer_service')
    CART = ('id', 'com.secoo:id/fl_detail_cart')
    ADD_CART_BTN = ('id', 'com.secoo:id/tv_buttom_left')
    BUY_NOW_BTN = ('id', 'com.secoo:id/tv_buttom_right')
    SURE_BUY_BTN = ('id', 'com.secoo:id/ll_buy')
    IV_COlOR = ('id', 'com.secoo:id/iv_color')
    INCREASE_BTN = ('id', 'com.secoo:id/iv_increase')
    SURE_ADD_BTN = ('id', 'com.secoo:id/ll_buy')
    SUCCESS_MSG = ('msg', ' 加入购物袋成功')

    @log_action
    def add_cart_new(self):
        logging.info("商品详情页，将商品加入购物车(新)")
        self.click(*self.ADD_CART_BTN)
        self.try_click(*self.IV_COlOR)
        self.try_click(*self.SURE_ADD_BTN)

    @log_action
    def view_cart(self):
        logging.info("查看购物袋")
        self.click(*self.CART)

    @log_action
    def buy_now(self):
        logging.info("立即购买")
        self.click(*self.BUY_NOW_BTN)
        self.try_click(*self.IV_COlOR)
        self.try_click(*self.SURE_BUY_BTN)


if __name__ == "__main__":
    from utils.device import boot_app
    from views.search.search_view import SearchView
    d = boot_app()
    s = SearchView(d)
    s.search('lv')
    s2 = GoodsDetailView(d)
    s2.add_cart_new()
