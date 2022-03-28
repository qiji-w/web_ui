# -*- coding:utf-8 -*- #
import time

import allure
import pytest

data = [('张三', '男'), ('李四', '女'), ('赵武', '男')]
data1 = ['case1', 'case2', 'case3']


@allure.feature("百度")
class TestDemo:
    @pytest.fixture()
    def board(self, init_driver):
        yield init_driver.jump_to_board_by_url()

    @pytest.mark.baidu
    @allure.story("百度demo")
    @pytest.mark.parametrize(["name", "sex"], data, ids=data1)
    def test_baidu(self, board, name, sex):
        res = board.send_text_click()
        print(name)
        print(sex)
        try:
            assert res
        except Exception as e:
            board.screen_shot_file(desc=f"demo错误")
            raise e

if __name__ == '__main__':
    pytest.main(["-s", "-v"])
