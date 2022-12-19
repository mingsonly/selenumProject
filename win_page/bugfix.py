# coding=utf-8
import requests


def request_api(meth, url, data=None, headers=None):
    req_type = meth.lower()
    request_type = {
        "get": requests.get(url, params=data, headers=headers),
        "post": requests.post(url, data, headers=headers)
    }
    res = request_type[req_type]
    print(res)


def request_sdk():
    url = 'http://10.35.2.222:10010/oauth/token?app_key=SDK_TOOLS'
    headers = {
        'tenant_id': "2",
        'app_key': "SDK_TOOLS",
        'Content-Type': "application/x-www-form-urlencoded",
    }
    data = {
        'user_id': "1337784078928703499",
        'client_id': "SDK_TOOLS",
        'client_secret': "U0RLX1RPT0xTOmdhbmd0aXNl",
        'grant_type': "client_credentials",
        'is_old_user': "0",
        'device_type': "201"

    }
    res = requests.post(url, data, headers=headers)
    print(res.text)


# Get方式调用platform-session-manage-service的http://容器组ip:10040/internal/data接口，查看返回结果，响应体中currentHandleMessageNum字段对应数据为0

def get_session():
    url = "http://10.35.1.210:10040/internal/data"
    ress = requests.get(url)
    print(ress.text)


if __name__ == '__main__':
    request_sdk()
    # get_session()
