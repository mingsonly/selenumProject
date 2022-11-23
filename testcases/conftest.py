# encoding: utf-8
# __author:  angel
# date:  2022/11/23

import pytest


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="输入要启动的浏览器")


@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")