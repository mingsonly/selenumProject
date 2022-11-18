# encoding: utf-8
# __author:  angel
# date:  2022/11/13
import random
import string
import pickle
import ddddocr


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
#     code = get_code('code.png')
#     print(code)