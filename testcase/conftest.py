# -*- coding:utf-8 -*- #
import sys
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

project_dir = os.path.dirname(os.path.dirname(__file__))

if project_dir not in sys.path:
    sys.path.append(project_dir)

browser = 'chrome'


@pytest.fixture(scope='session')
def init_driver():
    from page.op_base_page import OpBasePage
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'safari':
        driver = webdriver.Safari()
    elif browser == "headless":
        driver = webdriver.PhantomJS()
    elif browser == 'remote':
        options = Options()
        # 解决docker node chrome浏览器显示中文
        options.add_experimental_option('prefs', {'intl.accept_languages': 'zh-cn'})
        # capabilities.setdefault(Options.capabilities, options)
        driver = webdriver.Remote(command_executor='http://10.8.21.204:4445/wd/hub',
                                  desired_capabilities=options.to_capabilities())
    else:
        driver = ''
        print('浏览器类型暂不支持！！')
        sys.exit()
    init_driver = OpBasePage(driver)
    """打开页面进行登录"""
    # yield init_driver.open_op_url().login_op_by_gui(op_username, op_password)
    yield init_driver.open_op_url().login_baidu()

    # yield init_driver.open_op_url().login_op_by_api()
    time.sleep(5)
    init_driver.close_browser()


# 解决用例添加标签后出现的警告
def pytest_configure(config):
    """
    将添加的标签名放到marker_list中
    """
    marker_list = ['op_board', 'op_analysis', 'new_event_analysis', 'enterprise_overview', 'enterprise_users',
                   'platform_group', 'user_group', 'analysis_group', 'smoke']
    for markers in marker_list:
        config.addinivalue_line('markers', markers)


# 解决中文传参显示问题
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
