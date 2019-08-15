"""
购物车操作
@filename: cart_view.py
@author: hanzhichao
@date: 2019/01/07 13:34
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging


class CartView(Common):
    INCREASE_BTN = ('id', 'com.secoo:id/increase')
    CART_SUBMIT_BTN = ('id', 'com.secoo:id/cart_submit_order')

    def goto_settlement(self):
        logging.info("去结算")
        self.click(*self.CART_SUBMIT_BTN)


if __name__ == "__main__":
    from utils.device import boot_app
    from views.search.search_view import SearchView
    from views.goods.goods_detail_view import GoodsDetailView
    from views.mine.login_view import LoginView
    from views.order.settlement_view import SettlementView
    d = boot_app()
    s = SearchView(d)
    s.search('lv')
    s2 = GoodsDetailView(d)
    s2.add_cart_new()
    s2.view_cart()
    s3 = CartView(d)
    s3.goto_settlement()
    s4 = LoginView(d)
    s4.login_action("临渊羡鱼", "hanzhichao123")
    s5 = SettlementView(d)
    s5.submit_order()
