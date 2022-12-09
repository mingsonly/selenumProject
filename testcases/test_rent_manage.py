# coding=utf-8
import asyncio
import json

import requests
import socket
import time


class TestRentManage:
    def setup(self): pass

    def setup_class(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        pass

    def test_mock_user(self):
        url = "https://uat-platform.hongwuniu.com/application/thirdparty/login/tenantLogin?app_key=Mama_PC_67"
        mock_headers = {
            "Content-Type": "application/json",
            "app_key": "SDK_TOOLS",
            "timestamp": str(int(time.time()) * 1000),
            "nonce": "577",
            "signature": "$2a$10$/hjiFkXZWy2S3iy2KWZCuu7nDC5GgH4T3mM24hU/XQrX4TIRqxkqK",
            "tenant_id": "2"
        }
        data = [
            {
                "lang": "zh-cn",
                "gid": {
                    "fm": "tenant"
                },
                "http": [{
                    "gid": {
                        "name": "tenantCheck"
                    },
                    "type": "query",
                    "field": ["access_token", "token_type", "refresh_token", "expires_in", "tenantid", "deviceType",
                              "clientid", "tenantcode", "user_id"],
                    "condition": {
                        "must": [{
                            "term": {
                                "userid": "${__UUID}"
                            }
                        }, {
                            "term": {
                                "accesstoken": "123456"
                            }
                        }, {
                            "term": {
                                "env": "dev"
                            }
                        }]
                    }
                }]
            }
        ]
        res = requests.post(url, json=data, headers=mock_headers)
        self.web()

        return res

    def web(self):
        wss_url = "wss://uat-quote.hongwuniu.com:443/quote"
        web_data = {"type": "login", "gid": {"pg": "1", "idx": "1"}, "account": None, "userid": "64369555",
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjMxMTYsInVzZXJfdHlwZSI6MywiZXhwaXJlc19hdCI6MTY3MjYyODg3MDk4MiwiZGV2aWNlX2lkIjpudWxsLCJ1c2VyX2lkIjoiMTMwODk2NTUyOTY4NzIyODQxNiIsImRldmljZV90eXBlIjoiMjAxIiwiY2xpZW50X2lkIjoiTWFtYV9QQ182NyIsImhvc3RfaWRlbnRpZmllciI6ImFmZmQ3NDIzNWRkZDg4NzVmMGI3OWViNGI3MzQ4MTM4IiwianRpIjoiYWY1Zjc2NjAtMmMxOS00OWVmLWE3YmMtMTc3ODNkZDA4NjgwIn0.W8cCucntNZaKqmvG6WR2NkZRVZ8a9BP9WJmj47vwF-4",
                    "protocol": 1, "sdk": 1, "subscribe": ["quote"]}

        from websocket import create_connection
        import ssl
        wss = create_connection(wss_url,timeout=60,sslopt={"cert_reqs": ssl.CERT_NONE})
        print("==================")
        web_data = json.dumps(web_data, ensure_ascii=False)
        print(wss.status)
        wss.send(web_data)
        # print(wss.recv())


