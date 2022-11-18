# encoding: utf-8
# __author:  angel
# date:  2022/11/13


if __name__ == '__main__':
    arr = [5, 1, 2, 1, 4, 3, 5, 2, 14]
    def get_peak_ele(arr):
        result = []
        if arr[0] > arr[1]:
            result.append(arr[0])
        for i in range(1, len(arr) - 1):
            if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                result.append(arr[i])
        if arr[-1] > arr[-2]:
            result.append(arr[-1])
        return result
    result = get_peak_ele(arr)
    print(result)
