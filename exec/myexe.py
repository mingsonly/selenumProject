# encoding: utf-8
# __author:  angel
# date:  2022/11/25

# encoding: utf-8
# __author:  angel
# date:  2022/11/25


class LoginError(Exception):
    pass


class UserNameError(LoginError):
    def __str__(self):
        return "用户名错误"


class PassWordError(LoginError):
    def __str__(self):
        return "密码错误"


class PassWordInconsistency(LoginError):
    def __str__(self):
        return "两次密码不一致"
