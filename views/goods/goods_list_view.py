"""
商品详情操作
@filename: goods_detail_view.py
@author: hanzhichao
@date: 2019/01/07 11:13
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class GoodsListView(Common):
    FIRST_GOODS = ('id', 'com.secoo:id/icon')

    def click_first_goods(self):
        logging.info("商品列表页，点击第一个商品")
        self.click(*self.FIRST_GOODS)


if __name__ == "__main__":
    pass
