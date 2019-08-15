"""
我的页面操作
@filename: msg_center_view.py
@author: hanzhichao
@date: 2019/01/07 14:00
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class CartView(Common):
    MIME_ICO = ('id', "com.secoo:id/mine_circle_icon")
    NO_LOGIN_NAME = ('id', "com.secoo:id/vm_nologin_name")
    OBLIGATION = ('text', '待付款')
    ORDERS = ('id', 'com.secoo:id/order_top_orederid')
    CANCEL_ORDER_BTN = ('id', 'com.secoo:id/order_button_left')
    SURE_CANCLE_BTN = ('id', 'com.secoo:id/dialog_button_left')

    def view_obligation(self):
        logging.info("查看'待付款'")
        self.click(*self.OBLIGATION)

    def cancel_all_orders(self):
        logging.info("取消所有订单")
        orders = self.find_elements(*self.ORDERS)
        for order in orders:
            order.click()
            self.click(*self.CANCEL_ORDER_BTN)
            self.click(*self.SURE_CANCLE_BTN)
            self.driver.keyevent(4)


if __name__ == "__main__":
    pass