"""
结算中心操作
@filename: settlement_view.py
@author: hanzhichao
@date: 2019/01/07 13:34
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class SettlementView(Common):
    ORDER_SUBMIT_BTN = ('id', 'com.secoo:id/app_button_text')
    GOTO_PAY = ('id', 'com.secoo:id/textview_cashier_pay')
    # SURE_CANCEL_BTN = ('id', 'com.secoo:id/dialog_button_left')
    SURE_CANCEL_BTN = ('text', '确认离开')

    def submit_order(self):
        logging.info("提交订单")
        self.click(*self.ORDER_SUBMIT_BTN)

    def cancel_pay(self):
        logging.info("放弃支付")
        self.driver.keyevent(4)
        self.click(*self.SURE_CANCEL_BTN)


if __name__ == "__main__":
    pass
