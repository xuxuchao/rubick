"""
基本场景测试
@filename: test_basic_scenarios.py
@author: hanzhichao
@date: 2019/01/07 14:11
"""
import sys;sys.path.append("../..")
from time import sleep

from utils.log import log_docstring
from test_case.base_case import BaseCase
from views.home.home_view import HomeView
from views.category.category_view import CategoryView
from views.search.search_view import SearchView
from views.goods.goods_list_view import GoodsListView
from views.goods.goods_detail_view import GoodsDetailView
from views.cart.cart_view import CartView
from views.mine.login_view import LoginView
from views.order.settlement_view import SettlementView
from views.order.order_detail_view import OrderDetailView


class TestBasicScenarios(BaseCase):
    """基本场景测试"""

    @log_docstring
    def test_search_cart_login_submit_cancel_order(self):
        """
        搜索lv-第一个商品-添加购物车-购物车-去结算-提交-取消订单
        scenario
        """
        s = SearchView(self.driver)
        s.search('lv')
        s.click_first()
        s2 = GoodsDetailView(self.driver)
        s2.add_cart_new()
        s2.view_cart()
        s3 = CartView(self.driver)
        s3.goto_settlement()
        s4 = LoginView(self.driver)
        s4.login_action("临渊羡鱼", "hanzhichao123")
        s5 = SettlementView(self.driver)
        sleep(5)
        s5.submit_order()
        sleep(1)
        # 环境清理
        s5.cancel_pay()
        s6 = OrderDetailView(self.driver)
        s6.cancel_order()
        self.assertIsNotNone(s6.wait_toast("取消成功"))

    @log_docstring
    def test_category_buy_cancel_order(self):
        """
        分类-男包女包-女包-第一个商品-立即购买-提交-取消订单
        scenario
        """
        s1 = HomeView(self.driver)
        s1.boot_home()
        s1.click_category()
        s2 = CategoryView(self.driver)
        s2.select_female_bags()
        s3 = GoodsListView(self.driver)
        s3.click_first_goods()
        s4 = GoodsDetailView(self.driver)
        s4.buy_now()
        s5 = LoginView(self.driver)
        s5.login_action("临渊羡鱼", "hanzhichao123")
        s6 = SettlementView(self.driver)
        s6.submit_order()
        sleep(1)
        s6.cancel_pay()
        s7 = OrderDetailView(self.driver)
        s7.cancel_order()
        self.assertIsNotNone(s6.wait_toast("取消成功"))






