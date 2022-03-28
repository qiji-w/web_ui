# -*- coding:utf-8 -*- #
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from component.element_design import ElementDesign
from conf.conf import ERROR_IMAGE_PATH


class baiduPage(ElementDesign):
    # 元素
    Attribute_send_keys_id = (By.ID, 'kw')

    # 输入框输入内容，并点击确定
    def send_text_click(self):
        Attribute_id = self._find(self.Attribute_send_keys_id)
        Attribute_id.send_keys("十万个为什么")
        # self.screen_shot_file()
        # self._driver.get_screenshot_as_file(ERROR_IMAGE_PATH + r"\789.png")

        #TODO 数据效验  text/元素 用于assert
        return 1 == 2

