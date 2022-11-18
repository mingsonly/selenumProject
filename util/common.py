# encoding: utf-8
# __author:  angel
# date:  2022/11/13
import random
import string
import pickle
import ddddocr
import logging
import datetime
import logging.handlers


def get_logger():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler('error.log')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger


def get_code(path):
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


# if __name__ == '__main__':
#     logger = get_logger()
#     logger.warning("werwrw")
#     logger.error("eeroor")
#     code = get_code('code.png')
#     print(code)
