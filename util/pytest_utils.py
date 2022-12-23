# import re
# import pytest
# import logging
# import time
# from six.moves import input
#
# def execute_manual_step(info):
#
#     print(("\n[MANUAL STEP INFO] \n%s" % info))
#
#     """  Pauses test execution until user sets the step status.
#         见 https://stackoverflow.com/questions/62762845/attributeerror-module-pytest-has-no-attribute-config
#         pytest.config global was deprecated in pytest==4.0 and removed in pytest==5.0
#         所以相关用法需要根据 pytest 版本做判断
#     """
#
#     if pytest.__version__ >= "5.0":
#         from _pytest import config
#         PluginManager = config.PytestPluginManager()
#         capture_manager = PluginManager.getplugin(name='capturemanager')
#     else:
#         capture_manager = pytest.config.pluginmanager.getplugin('capturemanager')
#         capture_manager.suspend_global_capture(in_=True)
#
#     while True:
#         print("\nResult(符合上述描述输入 pass，不符合输入 fail):")
#         result = input().lower()
#         if result in ['no', 'fail', 'block']:
#             print("Comments 失败原因:")
#             comments = input()
#             if comments:
#                 break
#         elif result in ['yes', 'pass', 'p']:
#             break
#
#     if pytest.__version__ < "5.0":
#         capture_manager.resume_global_capture()
#
#     if result == 'fail':
#         logging.warning(comments)
#         pytest.fail(comments)
#     elif result == 'block':
#         logging.warning(comments)
#         pytest.skip(comments)
#
# def execute_manual_input(info):
#     # Pauses test execution until user input the value.
#     print(("\n[MANUAL INPUT INFO] \n%s" % info))
#
#     """
#         见 https://stackoverflow.com/questions/62762845/attributeerror-module-pytest-has-no-attribute-config
#         pytest.config global was deprecated in pytest==4.0 and removed in pytest==5.0
#         所以相关用法需要根据 pytest 版本做判断
#     """
#
#     if pytest.__version__ >= "5.0":
#         from _pytest import config
#         PluginManager = config.PytestPluginManager()
#         capture_manager = PluginManager.getplugin(name='capturemanager')
#     else:
#         capture_manager = pytest.config.pluginmanager.getplugin('capturemanager')
#         capture_manager.suspend_global_capture(in_=True)
#
#     print("\nInput:")
#     result = input()
#
#     return result
#
# def get_date():
#     timeArray = time.localtime(time.time())
#     otherStyleTime = time.strftime("_%y-%m-%d %H:%M", timeArray)
#     return otherStyleTime
#
# def print_dict(dict):
#     for key, value in dict.items():
#         print('{key}:{value}'.format(key=key, value=value))
#
#
# def generateTestTime(test_time):
#     if test_time is None:
#         for i in range(1000):
#             print("请正确填写pytest.ini里的'--testTime'")
#             time.sleep(3)
#     else:
#         assert re.match(r'\d{8}_\d{2}', test_time), "wrong testTime format"
#         return str(test_time)
