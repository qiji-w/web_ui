from component.element_design import ElementDesign
from page.demo.baidu.baidu_page import baiduPage


class HomePage(ElementDesign):

    def jump_to_board_by_url(self):
        return baiduPage(self._driver)
