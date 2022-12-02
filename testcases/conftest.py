# encoding: utf-8
# __author:  angel
# date:  2022/11/23

import pytest


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox", help="输入要启动的浏览器")
    parser.addoption("--env", action="store", default="test_env", help="输入被测环境")


@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture
def env(request):
    return request.config.getoption("--env")
