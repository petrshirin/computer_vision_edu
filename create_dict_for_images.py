import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.measure._regionprops import RegionProperties
from typing import Union


def has_bay(img_):
    invert_img = ~img_
    invert_img_zeros = np.zeros((invert_img.shape[0] + 1, invert_img.shape[1])).astype("uint8")
    invert_img_zeros[:-1, :] = invert_img
    return lakes(~invert_img_zeros) - 1


def count_bays(img_):
    return np.max(label(~img_.copy()))


def lakes(img_) -> int:
    invert_img = ~img_
    invert_img_ones = np.ones((invert_img.shape[0] + 2, invert_img.shape[1] + 2))
    invert_img_ones[1:-1, 1:-1] = invert_img
    return np.max(label(invert_img_ones)) - 1


def has_h_line(img_) -> bool:
    lines = np.sum(img_, 1) // img_.shape[1]
    return 1 in lines


def has_v_line(img_) -> bool:
    lines = np.sum(img_, 0) // img_.shape[0]
    return 1 in lines


def see_symbol(region: RegionProperties) -> Union[str, None]:
    region_lakes = lakes(region.image)
    if region_lakes == 0:
        if has_v_line(region.image):
            if np.all(region.image == 1):
                return '-'
            if count_bays(region.image) == 5:
                return '*'
            return '1'
        else:
            if count_bays(region.image) == 2:
                return '/'
            if count_bays(region.image) == 5:
                if has_h_line(region.image):
                    return '*'
                return 'W'
        if count_bays == 4 and (region.perimeter ** 2) / region.area > 40:
            return '*'
        else:
            return 'X'
    elif region_lakes == 1:
        if has_v_line(region.image):
            if count_bays(region.image) > 3:
                return '0'
            else:
                if (region.perimeter ** 2) / region.area < 59:
                    return 'P'
                else:
                    return 'D'
        else:
            if has_bay(region.image) > 0:
                return 'A'
            else:
                return '0'
    elif region_lakes == 2:
        if count_bays(region.image) > 4:
            return '8'
        else:
            return 'B'
    return None


def find_symbols(img_label_: np.ndarray):
    regions = regionprops(img_label_)

    symbol_dict = {}
    for region in regions:
        symbol = see_symbol(region)
        if symbol:
            if symbol not in symbol_dict:
                symbol_dict[symbol] = 1
            else:
                symbol_dict[symbol] += 1
    return symbol_dict


def view_percents(symbol_dict: dict, lab: np.ndarray) -> None:
    for key in symbol_dict.keys():
        symbol_dict[key] = symbol_dict[key] / np.max(lab) * 100
        print(f'{key}: {symbol_dict[key]}%')


if __name__ == '__main__':
    img = plt.imread("images/symbols.png")
    img = np.sum(img, 2)
    img[img > 0] = 1
    img_label = label(img)
    view_percents(find_symbols(img_label), img_label)
