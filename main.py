# encoding: utf-8
# __author:  angel
# date:  2022/11/13

from testcases import testcase1

if __name__ == '__main__':
    # testcase1.test2()

    arr = {13, 2, 4, 3, 11, 12, 3}


    def get_peak_ele(arr):
        result = []
        for i in range(len(arr)):
            if (i == 0 and arr[0] > arr[1]) or (i == len(arr) and arr[i]>arr[i-1]):
                result.append(arr[0])
            if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                result.append(arr[i])
        return result

    result = get_peak_ele(arr)