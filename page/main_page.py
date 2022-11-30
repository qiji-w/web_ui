# -*- coding:utf-8 -*- #
from component.element_design import ElementDesign
from conf.conf import main_module_path


class MainPage(ElementDesign):
    _path = main_module_path

    # 跳转某个模块
    def click_into_some_menu(self, first_menu: str, second_menu=None):
        pass