import math
import sys
import time
from time import sleep


import allure
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec, expected_conditions

# from selenium.webdriver import Remote  # selelnium-grid分布式打开浏览器使用的类
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from conf.conf import ERROR_IMAGE_PATH, LOG_PATH
from util.log import Logger
from util.util import element_add_screen_and_log

SHORT_TIMEOUT = 3
NORMAL_TIMEOUT = 6
LONG_TIMEOUT = 10
HUGE_TIMEOUT = 30

logger = Logger(LOG_PATH + 'error.log', level='error').logger


class BasePage:
    _url = ''
    _path = ''

    def __init__(self, driver: webdriver):

        self._driver = driver
        self._driver.maximize_window()
        self.set_implicitly_wait(LONG_TIMEOUT)
        if self._path != '':
            self.open_url()

    # 返回上一步
    def back_step(self, steps: int = 1):
        """返回上一步"""
        for i in range(steps):
            self._driver.back()

    # 设置隐式等待时间
    def set_implicitly_wait(self, second):
        """隐式等待"""
        self._driver.implicitly_wait(second)

    # 等待元素加载 - 显示等待
    def wait_presence(self, locator, timeout=10, poll=0.2):
        """
        :param locator: 元素表达式。格式为：('id', 'kw')
        :param timeout: 元素等待请求时间
        :param poll:    元素等待请求间隔时间
        :return:
        """
        try:
            wait = WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll)
            el = wait.until(expected_conditions.presence_of_element_located(locator))
            return el
        except Exception as e:
            logger.error("等待元素加载方法失败:", e)

    # 等待元素可以被点击方法
    def wait_clickable(self, locator, timeout=10, poll=0.2):
        """
        :param locator: 元素表达式。格式为：('id', 'kw')
        :param timeout: 元素等待请求时间
        :param poll:    元素等待请求间隔时间
        :return:
        """
        try:
            wait = WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll)
            el = wait.until(expected_conditions.element_to_be_clickable(locator))
            return el
        except Exception as e:
            logger.error("等待元素可以被点击方法失败:", e)

    # 显示等待查找元素 显示等待+条件判断，等到元素加载到dom中且可见
    def explicit_wait_util_ele_locate(self, locator, timeout) -> WebElement:
        """locator：元素定位器
            timeout：显示等待超时时间
        """
        return WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(locator), message="element not located!")

    # 打开网址
    def open_url(self):
        self._driver.get(self._url + self._path)
        return self

    # 打开path指定网页
    def open_url_inMiddle(self, path):
        self._driver.get(path)
        return self

    # 定位单一元素
    @element_add_screen_and_log
    def _find(self, locator, value: str = None, timeout=NORMAL_TIMEOUT) -> WebElement:
        """:param locator: 类型为tuple时，会默认按照显示等待去查找元素
            timeout: 显示等待超时时间 单位为秒
        """
        sleep(0.5)
        if isinstance(locator, tuple):
            # element = WebDriverWait(self._driver, 10).until(lambda driver: driver.find_element(*locator))
            element = self.explicit_wait_util_ele_locate(locator, timeout)
        else:
            element = self._driver.find_element(locator, value)
        return element

    # 在父元素中查找子元素
    @element_add_screen_and_log
    def _find_in_parent_ele(self, element: WebElement, locator) -> WebElement:
        """
        :param element: 查找的元素对象
        :param locator: 类型为tuple时，会默认按照显示等待去查找元素
        :param value: 元素定位方式
        :param timeout: 显示等待超时时间 单位为秒
        """
        sleep(1)
        return element.find_element(*locator)

    # 定位多个元素
    def _finds(self, locator, value: str = None) -> list:
        if isinstance(locator, tuple):
            return self._driver.find_elements(*locator)
        else:
            return self._driver.find_elements(locator, value)

    # 获取元素属性方法
    def get_attribute(self, locator, attr_name):
        """
        :param locator: 元素表达式。格式为：('id', 'kw')
        :param attr_name: html的属性，例： text  checked
        :return:
        """
        try:
            elem = self._driver.find_element(*locator)
            return elem.get_attribute(attr_name)
        except Exception as e:
            logger.error("获取元素属性方法失败:", e)

    # 获取元素的name属性方法
    @property
    def name(self, locator):
        """
        :param locator:  元素表达式。格式为：('id', 'kw')
        :return:
        """
        try:
            return self.get_attribute(locator, 'name')
        except Exception as e:
            logger.error("获取元素的name属性方法失败:", e)

    # 元素点击
    @element_add_screen_and_log
    def _element_click(self, element: WebElement):
        """元素点击"""
        element.click()

    # 元素输入内容
    @element_add_screen_and_log
    def _element_input(self, element: WebElement, input_content):
        element.send_keys(input_content)

    # 元素文案获取
    @element_add_screen_and_log
    def _element_get_text(self, element: WebElement):
        return element.text

    # 通用点击操作
    def click(self, locator, value: str = None, timeout=NORMAL_TIMEOUT):
        element = self._find(locator, value, timeout)
        self._element_click(element)

    # 通用输入操作
    def input_keys(self, locator, keys, value: str = None, advance_clear=False, timeout=LONG_TIMEOUT):

        """

        :param locator: 定位方式，可以是tuple或者str
                        eg：(By.CSS_SELECTOR, "#id_content")或者By.CSS_SELECTOR
        :param keys: 输入框内输入的内容
        :param value: 页面元素的定位方式，可以为空
        :param advance_clear: 标示符，输入内容之前是否要先清空，默认不清空
        :return:
        """
        element = self._find(locator, value, timeout)

        if advance_clear:
            element.send_keys(Keys.COMMAND, "a")
            element.send_keys(Keys.DELETE)
            self._element_input(element, keys)
        else:
            self._element_input(element, keys)

    # 获取元素文本
    def get_text(self, locator, value: str = None, timeout=LONG_TIMEOUT):

        element = self._find(locator, value, timeout)
        return self._element_get_text(element)

    # 滑动屏幕至目标元素展示在屏幕最底层
    def swipe_screen_bottom(self, ele: WebElement):
        self._driver.execute_script("arguments[0].scrollIntoView(false)", ele)

    # 滑动屏幕至目标元素展示在屏幕中间
    def swipe_screen_middle(self, ele: WebElement):
        self._driver.execute_script("arguments[0].scrollIntoView()", ele)

        # h5页面滚动条方法

    def scroll(self, options="scrollHeight", x=0, y=500):
        """

        :param options: 页面滚动方式
        :param x:       页面x坐标（像素)
        :param y:       页面x坐标（像素)
        :return:
        """
        try:
            # 页面向下滚动，滚动100像素
            if options == "scrollBy":
                return self._driver.execute_script(f"window.scrollTo({y})")
            # 页面向下滚动，默认滚动到页面中宽为0像素，长为500像素的位置
            elif options == "scrollTo":
                return self._driver.execute_script(f"window.scrollTo({x},{y})")
            # 页面向下滚动，滚动到当前加载出来页面的底部位置
            elif options == "scrollHeight":
                return self._driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # 页面向下滚动，滚动到当前加载出来页面的中间位置
            elif options == "scrollHeight2":
                return self._driver.execute_script("window.scrollTo(0,document.body.scrollHeight)/2")
            else:
                return "输入内容错误！"
        except Exception as e:
            print("h5页面滚动条方法失败:", e)
        # 将页面进行滑动，滑动到指定元素方法

    def location(self, el):
        try:
            return el.location_once_scrolled_into_view
        except Exception as e:
            logger.error('将页面进行滑动，滑动到指定元素方法失败:', e)

    # # 文件上传方法
    # def Desk(self, filename):
    #     """ 安装第三方库：pip install pywinauto -> from pywinauto import Desktop
    #     如果文件上传标签是input标签：使用send_keys()进行文件上传即可
    #     如果文件上传标签不是input标签，比如是div标签，只能借助第三方库pywinauto进行文件上传
    #     :param filename: 文件路径，例："E:\qqqq.pem"
    #     :return:
    #     """
    #     try:
    #         # ① 创建对象进行调用
    #         app = Desktop()
    #         # ② 根据选择文件系统弹窗的名字进入到系统弹窗内
    #         dialog = app['打开']
    #         # ③ 定位到输入框Edit，然后在输入框中输入上传文件的路径
    #         dialog["Edit"].TypeKeys(filename)
    #         # ④ 点击上传按钮进行上传
    #         dialog["Button"].click()
    #     except Exception as e:
    #         print("文件上传方法失败:", e)

    # 滑动屏幕
    # def swipe_screen(self):
    #     # 垂直滑动
    #     y_swipe = "document.documentElement.scrollTop={}"  # document.documentElement.scrollTop=800
    #     # 水平滑动
    #     x_swipe = "document.documentElement.scrollLeft={}"  # document.documentElement.scrollLeft=800
    #     # 滑动到指定坐标
    #     absolute_ordinate = "window.scrollTo(x, y)"  # window.scrollTo(0,100)
    #     # 滑动到相对坐标
    #     relative_ordinate = "window.scrollBy(x, y)"  # window.scrollBy(1,100)
    #     # 获取body高度滑到底部
    #     body_bottom = "window.scrollTo(0,document.body.scrollHeight)"
    #     # 获取body高度滑到顶部
    #     body_top = "window.scrollBy(0,100)"
    #
    #     self._driver.execute_script()

    # 处理alert、confirm、prompts
    def deal_accept_alert(self):
        alert = self._driver.switch_to.alert()
        alert.accept()

    # 处理alert、confirm、prompts
    def deal_dismiss_alert(self):
        alert = self._driver.switch_to.alert()
        alert.dismiss()

    # alert输入内容并点击确认方法
    def deal_sendKeys_accept_alert(self, text):
        try:
            self._driver.switch_to.alert.send_keys(text)
            self._driver.switch_to.alert.accept()
            return self
        except Exception as e:
            logger.error("alert输入输入内容并点击确认方法失败:", e)

    # 切换新窗口
    def switch_to_windows(self):
        try:
            window = self._driver.window_handles
            return self._driver.switch_to.windows(window[-1])
        except Exception as e:
            logger.error("切换新窗口方法失败:", e)

    # 鼠标移动悬停事件
    def move_mouse_stop(self, locator):
        """鼠标悬停"""
        ActionChains(self._driver).move_to_element(self._find(locator)).perform()

    # 切换窗口聚柄
    def switch_to_window_by_title(self, window_title):
        """window_title: 窗口title"""
        sleep(2)
        all_handles = self._driver.window_handles
        for window_handle in all_handles:
            self.switch_to_target_window(window_handle)
            if self._driver.title == window_title:
                return
        raise Exception("不存在目标窗口，切换窗口句柄失败！")

    # 切换到某个窗口
    def switch_to_target_window(self, window_handle):
        """window_handle：窗口聚柄"""
        self._driver.switch_to_window(window_handle)

    # 获取当前窗口聚柄
    def get_current_window_handle(self):
        return self._driver.current_window_handle

    # 获取所有窗口的句柄
    def get_all_handles(self) -> list:
        return self._driver.window_handles

    # 切换frame
    def switch_to_target_frame(self, frame_reference):
        """
        eg:
            driver.switch_to.frame('frame_name')
            driver.switch_to.frame(1)
            driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        """
        self._driver.switch_to_frame(frame_reference)

    # 切换到默认frame
    def switch_to_default_frame(self):
        self._driver.switch_to.default_content()

    # 切换到父frame
    def switch_to_parent_frame(self):
        self._driver.switch_to.parent_frame()

    # iframe切换方法 - 显示等待
    def switch_to_frame(self, reference=None, timeout=10, poll=0.2):
        """
        :param reference: reference=None返回最外层，reference=iframe元素，切换至iframe页面
        :param timeout: 元素等待请求时间
        :param poll: 元素等待请求间隔时间
        :return:
        """
        try:
            if not reference:
                return self._driver.switch_to.default_content()
            wait = WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll)
            el = wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(reference))
            return el
        except Exception as e:
            logger.error("iframe切换方法失败:", e)

    # 鼠标事件 双击
    def mouse_double_click(self, element):
        """鼠标双击"""
        ActionChains(self._driver).double_click(element).perform()

    # 右击
    def mouse_right_click(self, element):
        """鼠标右击"""
        ActionChains(self._driver).context_click(element).perform()

    # 拖动
    def mouse_drag_drop(self, source_ele, target_ele):
        """拖动某个元素到某个元素上"""
        ActionChains(self._driver).drag_and_drop(source_ele, target_ele).perform()

    # 鼠标悬停
    def mouse_stop_element(self, target_ele: WebElement):
        """鼠标悬停"""
        ActionChains(self._driver).move_to_element(target_ele).perform()

    # 键盘事件 输入回车内容
    def send_enter(self, ele):
        ele.send_keys(Keys.ENTER)

    # 输入空格
    def send_space(self, ele: WebElement):
        ele.send_keys(Keys.SPACE)

    # mac 输入command + a 全选
    def send_command_with_A(self, ele: WebElement):
        if sys.platform == 'darwin':
            ele.send_keys(Keys.COMMAND, "a")
        else:
            ele.send_keys(Keys.CONTROL + "a")

    # 输入删除
    def send_back_space(self, ele: WebElement):
        ele.send_keys(Keys.BACK_SPACE)

    # 输入制表符
    def send_tab(self, ele: WebElement):
        ele.send_keys(Keys.TAB)

    # 截屏
    def screen_shot(self):
        return self._driver.get_screenshot_as_png()

    # 截屏存储
    def screen_shot_file(self, desc="None"):
        try:
            name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + desc + ".png"
            self._driver.get_screenshot_as_file(ERROR_IMAGE_PATH + f"{name}")
            allure.attach(body=self.screen_shot(), name=desc,
                          attachment_type="png")

        except Exception as e:
            logger.error("截图存放，添加到allure报告的附件上去失败:", e)

    # 关闭浏览器
    def close_browser(self):
        self._driver.quit()

    # ############################appium##################################
    # 向元素输入内容操作(用时需要填写切换自带输入法)
    def inputCh(self, el, text):
        """

        :param el: 元素
        :param text: 文本内容
        :return:
        """
        try:

            self._driver.activate_ime_engine('io.ui_pytest_demo_master.android.ime/.UnicodeIME')

            el.send_keys(text)
            # self._driver.activate_ime_engine('io.ui_pytest_demo_master.android.ime/.UnicodeIME')
        except Exception as e:
            logger.error("切换输入法输入内容失败:", e)

    # toast提示吐司操作
    def toastAction(self, text):
        """

        :param text: 文本内容
        :return:
        """

        xpath = (By.XPATH, f'//*[contains(@text,"{text}")]')

        try:

            toast = WebDriverWait(driver=self._driver, timeout=5, poll_frequency=0.1).until(
                presence_of_element_located(xpath))
            return toast
        except Exception as e:

            logger.error('未获取到吐司:', e)

    # 根据绝对坐标点击操作
    def clickXY(self, x, y):
        """

        :param x: 坐标x
        :param y: 坐标y
        :return:
        """
        try:
            TouchAction(self._driver).tap(x=x, y=y).release().perform()
        except Exception as e:
            logger.error('根据绝对坐标点击操作失败:', e)

    # 根据相对坐标点击操作
    def clickPos(self, p):
        """
        相对坐标*屏幕大小为绝对坐标（绝对坐标需要取整！）
        :param p: weditor相对坐标 ，例：p = (0.489, 0.911)
        :return:
        """
        try:
            s = self.getSize()
            x1 = math.ceil(p[0] * s[0])
            y1 = math.ceil(p[1] * s[1])
            TouchAction(self._driver).tap(x=x1, y=y1).perform()
        except Exception as e:
            logger.error('根据绝对坐标点击操作失败:', e)

    # 双指放大/缩小
    def pinch(self, direction="on", offset=0.2):
        """

        :param direction: 移动方向
        :param offset: 移动像素点，比如： offset=0.2
        :return:
        """
        s = self.getSize()

        if direction == "in":
            action_1 = TouchAction(self._driver)
            action_1.press(x=s[0] / 2, y=s[1] / 2).move_to(
                x=s[0] / 2, y=s[1] / 2 - offset).release()
            action_2 = TouchAction(self._driver)
            action_2.press(x=s[0] / 2, y=s[1] / 2).move_to(
                x=s[0] / 2, y=s[1] / 2 + offset).release()

            m = MultiAction(self._driver)
            m.add(action_1, action_2)
            m.perform()

        elif direction == "on":
            action_1 = TouchAction(self._driver)
            action_1.press(x=s[0] / 2, y=s[1] / 2 - offset).move_to(
                x=s[0] / 2, y=s[1] / 2).release()
            action_2 = TouchAction(self._driver)
            action_2.press(x=s[0] / 2, y=s[1] / 2 + offset).move_to(
                x=s[0] / 2, y=s[1] / 2).release()

            m = MultiAction(self._driver)
            m.add(action_1, action_2)
            m.perform()

        else:
            return "输入格式错误"

    # 获取当前手机的屏幕绝对大小值方法
    def getSize(self):
        s = self._driver.get_window_size()
        return s['width'], s['height']

    # 上下左右滑动方法
    def swipeXY(self, direction="right"):
        if direction == 'left':
            return self.swipeLeft(heng_percent=0.9, shu_percent=0.5)
        elif direction == 'right':
            return self.swipeRight(heng_percent=0.1, shu_percent=0.5)
        elif direction == 'up':
            return self.swipeUp(heng_percent=0.5, shu_percent=0.9)
        elif direction == 'down':
            return self.swipeDown(heng_percent=0.5, shu_percent=0.1)
        else:
            return "输入格式错误"

    # 九宫格函数方法
    def jiu_rect(self, pos=1, els=None):
        """

        :param pos: 九宫格，坐标点（1-9）
        :param els: 九宫格元素
        :return:
        """
        el = self._driver.find_element(By.XPATH, els)
        rect = el.rect
        start_x = rect['x']
        start_y = rect['y']
        width = rect['width']
        height = rect['height']
        if pos == 1:
            point_01 = {'x': start_x + width * 1 / 6, 'y': start_y + height * 1 / 6}
            return point_01

        elif pos == 2:
            point_02 = {'x': start_x + width * 1 / 2, 'y': start_y + height * 1 / 6}
            return point_02

        elif pos == 3:
            point_03 = {'x': start_x + width * 5 / 6, 'y': start_y + height * 1 / 6}
            return point_03

        elif pos == 4:
            point_04 = {'x': start_x + width * 1 / 6, 'y': start_y + height * 1 / 2}
            return point_04

        elif pos == 5:
            point_05 = {'x': start_x + width * 1 / 2, 'y': start_y + height * 1 / 2}
            return point_05

        elif pos == 6:
            point_06 = {'x': start_x + width * 5 / 6, 'y': start_y + height * 1 / 2}
            return point_06

        elif pos == 7:
            point_07 = {'x': start_x + width * 1 / 6, 'y': start_y + height * 5 / 6}
            return point_07

        elif pos == 8:
            point_08 = {'x': start_x + width * 1 / 2, 'y': start_y + height * 5 / 6}
            return point_08

        elif pos == 9:

            point_09 = {'x': start_x + width * 5 / 6, 'y': start_y + height * 5 / 6}
            return point_09
        else:
            return "输入格式错误"

    # 右滑操作方法
    def swipeRight(self, heng_percent=0.1, shu_percent=0.5):
        """
        坐标X、Y值如果都是0，那坐标点就是屏幕左上角(0,0)
        :param driver: driver驱动 ，必填
        :param heng_percent: 横向百分比，选填
        :param shu_percent: 纵向百分比，选填
        :return:
        """
        try:
            s = self.getSize()
            x1 = s[0] * heng_percent
            x2 = s[0] * (1 - heng_percent)
            y = s[1] * shu_percent
            self._driver.swipe(x1, y, x2, y, 2000)
        except Exception as e:
            logger.error("右滑操作失败:", e)

    # 左滑操作方法
    def swipeLeft(self, heng_percent=0.9, shu_percent=0.5):

        try:
            s = self.getSize()

            x1 = s[0] * heng_percent

            x2 = s[0] * (1 - heng_percent)

            y = s[1] * shu_percent
            self._driver.swipe(x1, y, x2, y, 2000)
        except Exception as e:
            logger.error("左滑操作失败:", e)

    # 下滑操作方法
    def swipeDown(self, heng_percent=0.5, shu_percent=0.1):

        try:
            s = self.getSize()
            x = s[0] * heng_percent
            y1 = s[1] * shu_percent
            y2 = s[1] * (1 - shu_percent)
            self._driver.swipe(x, y1, x, y2, 2000)
        except Exception as e:
            logger.error("下滑操作失败:", e)

    # 上滑操作方法
    def swipeUp(self, heng_percent=0.5, shu_percent=0.9):

        try:
            s = self.getSize()
            x = s[0] * heng_percent
            y1 = s[1] * shu_percent
            y2 = s[1] * (1 - shu_percent)
            self._driver.swipe(x, y1, x, y2, 2000)
        except Exception as e:
            logger.error("上滑操作失败:", e)


if __name__ == '__main__':
    logger.error("1")
