#coding=utf-8
import pytest
import logging
from six.moves import input


def execute_manual_step(info):
    print(("\n[MANUAL STEP INFO] \n%s" % info))

    """  Pauses test execution until user sets the step status.
        见 https://stackoverflow.com/questions/62762845/attributeerror-module-pytest-has-no-attribute-config
        pytest.config global was deprecated in pytest==4.0 and removed in pytest==5.0
        所以相关用法需要根据 pytest 版本做判断
    """

    if pytest.__version__ >= "5.0":
        from _pytest import config
        PluginManager = config.PytestPluginManager()
        capture_manager = PluginManager.getplugin(name='capturemanager')
    else:
        capture_manager = pytest.config.pluginmanager.getplugin('capturemanager')
        capture_manager.suspend_global_capture(in_=True)
    comments = ""
    while True:
        print("\nResult(符合上述描述输入 pass or p，不符合输入 fail or block):")
        user_cmd = input()
        result = user_cmd.lower()
        if result in ['fail', 'block']:
            print("Comments 失败原因:")
            comments = input()
            if comments:
                break
        elif result in ['pass', 'p']:
            break

    if pytest.__version__ < "5.0":
        capture_manager.resume_global_capture()

    if result == 'fail':
        logging.warning(comments)
        pytest.fail(comments)
    elif result == 'block':
        logging.warning(comments)
        pytest.skip(comments)
