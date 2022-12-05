import pytest
import os
import time


def run(file):
    pytest.main(['--alluredir', '../reports', file])


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    for _, _, files in os.walk(path):
        for file in files:
            if file.startswith("test_"):
                run(file)
    os.system("allure serve ../reports")
