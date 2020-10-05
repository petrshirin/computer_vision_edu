from task1_1 import read_data
from typing import List

FILE_NAME_1 = 'C:/Users/Admin/Downloads/img1.txt'
FILE_NAME_2 = 'C:/Users/Admin/Downloads/img2.txt'


def calculate_offset(data1: List[List[int]], data2: List[List[int]]) -> List[int]:
    x1, y1 = -1, -1
    x2, y2 = -1, -1
    for i in range(len(data1)):
        if x1 != -1 and y1 != -1:
            break
        for j in range(len(data1[i])):
            if data1[i][j]:
                x1, y1 = i, j

    for i in range(len(data2)):
        if x2 != -1 and y2 != -1:
            break
        for j in range(len(data2[i])):
            if data2[i][j]:
                x2, y2 = i, j
    return [abs(x1 - x2), abs(y1 - y2)]


if __name__ == '__main__':
    figure1 = read_data(FILE_NAME_1)
    figure2 = read_data(FILE_NAME_2)
    result = calculate_offset(figure1['array'], figure2['array'])
    print(f"x: {result[0]} y: {result[1]}")
