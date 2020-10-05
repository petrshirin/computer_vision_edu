import numpy
import matplotlib.pyplot as plt
from typing import Dict


FILE_NAMES = ['C:/Users/Admin/Downloads/figure1.txt',
              'C:/Users/Admin/Downloads/figure2.txt',
              'C:/Users/Admin/Downloads/figure3.txt',
              'C:/Users/Admin/Downloads/figure4.txt',
              'C:/Users/Admin/Downloads/figure5.txt',
              'C:/Users/Admin/Downloads/figure6.txt',]


def read_data(file_name: str) -> Dict:
    return_array = []
    with open(file_name, 'r') as f:
        data = f.read()
    splited_data = data.split('\n')
    resolution = float(splited_data[0])
    for row in splited_data[2:-1]:

        splited_row = row.split(' ')
        return_array.append(list(map(int, splited_row[:-1])))
    return {"resolution": resolution, "array": return_array}


def get_mm_resolution(data: numpy.array):
    max_size = 0
    for row in data:
        if sum(row) > max_size:
            max_size = sum(row)
    return max_size


if __name__ == '__main__':
    for file_path in FILE_NAMES:
        figure_info = read_data(file_path)
        print(figure_info['resolution'] / get_mm_resolution(figure_info['array']))


