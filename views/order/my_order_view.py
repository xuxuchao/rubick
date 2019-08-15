"""
订单详情页操作
@filename: my_order_view.py
@author: hanzhichao
@date: 2019/01/07 15:17
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class OrderDetailView(Common):
    CANCEL_ORDER_BTN = ('id', 'com.secoo:id/order_button_left')
    SURE_CANCEL_BTN = ('id', 'com.secoo:id/dialog_button_left')

    def cancel_order(self):
        logging.info("取消订单")
        self.click(*self.CANCEL_ORDER_BTN)
        self.click(*self.SURE_CANCEL_BTN)


if __name__ == "__main__":
    pass
