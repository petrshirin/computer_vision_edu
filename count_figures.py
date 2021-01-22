import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.measure import label, regionprops
from typing import Tuple, List


def find_figures(img_: np.ndarray) -> Tuple[List, List]:
    circles = []
    rectangles = []
    for c in color:
        circles.append({c: []})
        rectangles.append({c: []})
        new_image = img_.copy()
        new_image[new_image != c] = 0
        lab = label(new_image)
        reg = regionprops(lab)
        for s in reg:
            if np.all(s.image):
                circles[-1][c].append(s)
            else:
                rectangles[-1][c].append(s)
    return circles, rectangles


if __name__ == '__main__':
    img = plt.imread("images/balls_and_rects.png")
    img = color.rgb2hsv(img)[:, :, 0]
    unique_values = np.unique(img) * 10
    img = np.ceil(img * 10)
    unique_values = np.ceil(unique_values)
    color = np.unique(unique_values)
    circles, rectangles = find_figures(img)
    full_len = 0
    for circle in circles:
        key = list(circle.keys())[0]
        print(f'color: {key}', len(circle[key]))
        full_len += len(circle[key])
    for rectangle in rectangles:
        key = list(rectangle.keys())[0]
        print(f'color: {key}', len(rectangle[key]))
        full_len += len(rectangle[key])
    print(f'full len = {full_len}')

