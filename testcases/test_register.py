# encoding: utf-8
# __author:  angel
# date:  2022/11/13

import allure
import pytest


class TestRegister(object):
    def setup(self):
        pass

    def setup_class(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("打开注册页面")
    def test_01(self):
        print("test01....")



if __name__ == '__main__':
    # pytest.main(['-svq', 'test_register.py'])
    # pytest.main(['-sq', 'test_register.py'])
    pytest.main(['--alluredir',"../reports", 'test_register.py'])
