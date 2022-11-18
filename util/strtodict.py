from selenium import webdriver
from selenium.webdriver.common.by import By


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, *loc):
        ele = self.driver.find_element(*loc)
        return ele

    def clear(self, *loc):
        self.find_element(*loc).clear()

    def type_text(self, text, *loc):
        self.clear(*loc)
        self.driver.find_element(*loc).send_keys(text)

    def close(self):
        self.driver.close()


class LoginPage(BasePage):
    url = ""
    name_loc = (By.XPATH,"xxx")
    pwd_loc = (By.ID, "pwd")

    def __init__(self, driver):
        super().__init__(driver)


    def input_name(self,username):
        self.type_text(username, self.name_loc)



def fib(n):
    if n<2:
        return n
    return fib(n-1) + fib(n-2)
if __name__ == '__main__':



    total = fib(3)

# import requests
#
#
# class BaseData:
#     _field = []
#
#     def __init__(self, *args, **kwargs):
#         if len(args) > len(self._field):
#             raise TypeError(f"Expected {len(self.field)} Params!!!")
#         for name, value in zip(self._field, args):
#             setattr(self, name, value)
#         for name in self._field[len(args):]:
#             if name in kwargs:
#                 setattr(self, name, kwargs.pop(name))
#         if kwargs:
#             raise KeyError(f'Invalid Param(s):{kwargs}！')
#
#     def request_api(self, url, meth: str, data, headers):
#         meth = meth.lower()
#         request_type = {
#             "get": requests.get,
#             "post": requests.post,
#         }
#         res = request_type[meth](url, data, headers=headers)
#         return res
#
#
# class KTV(BaseData):
#     _field = ['name', 'age', 'score']
#
#
# if __name__ == '__main__':
#     ktv = KTV('xiaoli', 18, age=19)
#     data = {}
#     url = "xxxx"
#     res = ktv.request_api("get",url, ktv.__dict__, headers={})
