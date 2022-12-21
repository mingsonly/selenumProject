# encoding: utf-8
# __author:  angel
# date:  2022/11/13
import random
import string
import pickle
import ddddocr
import logging
import logging.handlers
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import uuid
import time
from functools import wraps
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")
data_dir = os.path.join(os.path.dirname(cur_dir), "data")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

import json


def get_env_data(env="test_env"):
    """根据环境参数参数决定读取哪个环境的配置文件"""
    path = os.path.join(data_dir, env + ".json")
    with open(path, "r") as f:
        test_data = json.load(f)
    return test_data


def start_webdriver(web="chrome"):
    browsers = {
        "chrome": webdriver.Chrome,
        "firefox": webdriver.Firefox
    }
    return browsers[web]()


def get_logger():
    all_log_path = os.path.join(log_dir, "all.log")
    err_log_path = os.path.join(log_dir, "error.log")

    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler(all_log_path, when='midnight', interval=1, backupCount=7)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler(err_log_path)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger


def get_img_code(id, driver):
    """通过元素位置截取验证码图片"""
    t = time.time()
    img_name = img_dir + "\\" + str(t) + ".png"
    driver.save_screenshot(img_name)
    ce = driver.find_element(by=By.ID, value=id)

    left = ce.location['x']
    top = ce.location['y']
    right = ce.size['width'] + left
    height = ce.size['height'] + top

    im = Image.open(img_name)
    img = im.scrop((left, top, right, height))
    t = time.time()
    picture_name = img_dir + "\\" + str(t) + ".png"
    img.save(picture_name)


def get_code(path):
    """通过第三方模块识别图片获取验证码
    :param path: 图片地址
    :return code,图片验证码
    """
    with open(path, 'rb') as f:
        img_bytes = f.read()
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(img_bytes)
    return code


def gen_random_str(size=8):
    """生成随机字符串"""
    # ascii_letters 字母+digits数字组合
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, size))
    return rand_str


def save_cookie(driver, path):
    with open(path, 'wb') as f:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies, f)


def load_cookie(drive, path):
    with open(path, 'rb') as cookiefile:
        cookies = pickle.load(cookiefile)
        for cookie in cookies:
            drive.add_cookie(cookie)


def get_session():
    uat_cloud_path = os.path.join(data_dir, "uat_cloud.json")
    with open(uat_cloud_path, "r") as f:
        cloud_data = json.load(f)

    s = requests.session()
    timestamp = int(time.time()) * 1000
    res = s.post(cloud_data['url'] + f"{timestamp}", cloud_data['data'], verify=False)
    s.headers['Authorization'] = "Bearer " + res.json()['access_token']
    # todo 此处如果报未知错误，是因为传输数据得格式因为 json=data
    return s.headers


def fetch_status_code(func):
    """
    在日志文件中匹配错误状态码
    :param func 业务函数对象
    :return: mydecorate 装饰过后得函数对象
    """

    @wraps(func)
    def fetch_log_msg(*args, **kwargs):
        time_str = str(int(time.time()))[7:]
        log_path = os.path.join(log_dir, f"status_code_{time_str}.log")
        execute_cmd_commind("logcat")
        re_pattern = func(*args, **kwargs)
        execute_cmd_commind("adb_close", log_path)
        result = fetch_code(re_pattern)
        return result

    return fetch_log_msg

time_str = str(int(time.time()))[7:]
log_path = os.path.join(log_dir, f"status_code_{time_str}.log")
def fetch_code(pattern):
    result = []
    with open(log_path, "rt", encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            line = line.replace('\\', "").strip()
            if re.findall(pattern, line):
                result.append({line[:18]: line})
    return result


def execute_cmd_commind(cmd):
    cmds = {
        "logcat": f"adb logcat -v time > {log_path}",
        "adb_close": "taskkill /f /t /im adb.exe"
    }
    os.popen(cmds[cmd])

# if __name__ == '__main__':
#     import os
#
#     pattern = "1002001005"
#     fecth = fetch_code(pattern, "1220_01.txt")
#     print(fecth)
# for i in fecth:
#     print(i)
