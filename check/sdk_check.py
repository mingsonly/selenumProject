# coding=utf-8

def search_check(expect_val: str, actual_vals: list):
    """
    校验检查点是否在result中
    :param check_point,股票代码
    :param stocks,股票查询结果集合
    :return: True or False
    """
    result = False
    for actual in actual_vals:
        if expect_val in actual.keys():
            result = True
    return result









if __name__ == '__main__':
    stocks = [
        {"000001.SZ": "平安银行"},
        {"000002.SZ": "万 科A"},
        {"000004.SZ": "ST国华"},
        {"000005.SZ": "ST星源"},
    ]
    flag = search_check("00000.SZ", stocks)
    print(flag)
