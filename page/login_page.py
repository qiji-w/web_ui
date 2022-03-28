# -*- coding:utf-8 -*- #
from selenium.webdriver.common.by import By

from conf.conf import login_path
from component.element_design import ElementDesign
from page.home_page import HomePage


class OpLoginPage(ElementDesign):
    # _path = '/login'
    _path = login_path
    _username_element_locator = (By.ID, 'identity')
    _password_element_locator = (By.ID, 'password')
    _submit_element_locator = (By.XPATH, '//button[@type="button"]')

    # 通过UI页面登陆
    def login_op_by_gui(self, username, password):
        self.input_keys(self._username_element_locator, username)
        self.input_keys(self._password_element_locator, password)

        self.click(self._submit_element_locator)

        self.add_cookies_by_gui()

        return HomePage(self._driver)

    # 通过api登陆
    def login_op_by_api(self):

        self.add_cookies_by_api()

        return HomePage(self._driver)

    def login_baidu(self):
        # 这里必须进行driver的初始化设置
        return HomePage(self._driver)
