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

cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(os.path.dirname(cur_dir), "logs")
img_dir = os.path.join(os.path.dirname(cur_dir), "screenshots")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)


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


def gen_random_str():
    # ascii_letters 字母+digits数字组合
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
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
