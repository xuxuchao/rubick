"""
分类页面操作
@filename: category_view.py
@author: hanzhichao
@date: 2019/01/07 15:41
"""
import sys; sys.path.append("..")

from views.common_view import Common
from utils.log import logging, log_action


class CategoryView(Common):
    MALE_FEMAIL_BAGS = ('text', "男包女包")
    FEMAIL_BAGS = ('text', '女包')

    @log_action
    def select_female_bags(self):
        logging.info("选择'女包'")
        self.click(*self.MALE_FEMAIL_BAGS)
        self.click(*self.FEMAIL_BAGS)


if __name__ == "__main__":
    pass
