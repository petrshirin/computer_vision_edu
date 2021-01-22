import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
from skimage.filters import threshold_triangle
from skimage.measure import (label, regionprops)
from skimage.measure._regionprops import RegionProperties
from typing import Union, List


def to_gray(img: ndarray):
    return (0.2989 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]).astype("uint8")


def image_to_binary(img: ndarray,
                    limit_min: Union[float, int],
                    limit_max: Union[float, int]):
    bin_img = img.copy()
    bin_img[bin_img <= limit_min] = 0
    bin_img[bin_img >= limit_max] = 0
    bin_img[bin_img > 0] = 1
    return bin_img


def process_image(image_path: str) -> ndarray:
    img = plt.imread(image_path)
    img_gray = to_gray(img)
    pencil_triangle = threshold_triangle(img_gray)
    binary_img = image_to_binary(img_gray, 0, pencil_triangle)
    binary_img = morphology.binary_dilation(binary_img, iterations=1)
    return binary_img


def read_images(base_dir: str) -> List[ndarray]:
    images = []
    for img_num in range(1, 13):
        images.append(process_image(f'{base_dir}/img ({img_num}).jpg'))

    return images


def find_areas(img_labels: ndarray) -> List[RegionProperties]:
    areas = []

    for region in regionprops(img_labels):
        areas.append(region.area)

    return areas


def calculate_pencils() -> int:
    count_pencils = 0
    for img in read_images('images/'):
        img_labels = label(img)
        areas = find_areas(img_labels)
        print(img_labels)

        for region in regionprops(img_labels):
            if region.area < np.mean(areas):
                img_labels[img_labels == region.label] = 0
            bbox = region.bbox
            if bbox[0] == 0 or bbox[1] == 0:
                img_labels[img_labels == region.label] = 0

        img_labels[img_labels > 0] = 1
        img_labels = label(img_labels)
        print(img_labels)

        for region in regionprops(img_labels):
            if (region.perimeter ** 2 / region.area > 100) and (300000 < region.area < 450000):
                count_pencils += 1

    return count_pencils


if __name__ == '__main__':
    print(calculate_pencils())
