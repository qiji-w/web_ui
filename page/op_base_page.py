from time import sleep

from basepage.base_page import BasePage
from conf.conf import base_url, op_username, op_password
from util.util import GetOpCookies


class OpBasePage(BasePage):
    # op网址
    _url = base_url

    def add_cookies_by_gui(self):
        sleep(1)
        cookies = self._driver.get_cookies()
        # print(cookies)
        for per_cookie in cookies:
            self._driver.add_cookie(cookie_dict=per_cookie)

    def add_cookies_by_api(self):
        cookies = GetOpCookies().get_op_uat_cookies(op_username, op_password, self._url)  # 使用API获取cookie
        # print(cookies)
        for per_cookie in cookies:
            self._driver.add_cookie(cookie_dict=per_cookie)

    # 打开op网站
    def open_op_url(self):
        from page.login_page import OpLoginPage

        self._driver.get("https://www.baidu.com/")
        return OpLoginPage(self._driver)
