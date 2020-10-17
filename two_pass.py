import numpy as np
import matplotlib.pyplot as plt


def negate(bin_image: np.ndarray):
    arr = bin_image.copy()
    arr[np.where(arr == 1)] = -1
    return arr


def neighbours2(bin_image: np.ndarray, y, x):
    left = y, x - 1
    top = y - 1, x
    if not check(bin_image, *left):
        left = None
    if not check(bin_image, *top):
        top = None
    return left, top


def check(bin_image: np.ndarray, y, x):
    if not 0 <= y < bin_image.shape[0]:
        return False
    if not 0 <= x < bin_image.shape[1]:
        return False
    if bin_image[y, x] != 0:
        return True
    return False


def exists(neighbours):
    return not all([n is None for n in neighbours])


def find(label, links):
    j = label
    while links[j] != 0:
        j = links[j]
    return j


def union(label1, label2, links):
    r1 = find(label1, links)
    r2 = find(label2, links)
    if r1 != r2:
        links[r2] = r1


def two_pass_labeling(bin_image: np.ndarray) -> np.ndarray:
    links: np.ndarray = np.zeros(len(bin_image)).astype("uint32")
    labels: np.ndarray = np.zeros_like(bin_image).astype("uint32")
    label = 1
    for y in range(bin_image.shape[0]):
        for x in range(bin_image.shape[1]):
            if bin_image[y, x] != 0:
                n = neighbours2(bin_image, y, x)
                if not exists(n):
                    m = label
                    label += 1
                else:
                    lbs = [labels[i] for i in n if i is not None]
                    m = min(lbs)
                labels[y, x] = m
                for i in n:
                    if i is not None:
                        lb = labels[i]
                        if lb != m:
                            union(m, lb, links)
    for y in range(bin_image.shape[0]):
        for x in range(bin_image.shape[1]):
            if labels[y, x] != 0:
                new_label = find(labels[y, x], links)
                if new_label != labels[y, x]:
                    labels[y, x] = new_label
    quantity = 0
    lb_unique = np.unique(labels)
    for i in lb_unique:
        labels[labels == i] = quantity
        quantity += 1
    return labels


if __name__ == "__main__":
    B = np.zeros((20, 20), dtype='int32')

    B[1:-1, -2] = 1

    B[1, 1:5] = 1
    B[1, 7:12] = 1
    B[2, 1:3] = 1
    B[2, 6:8] = 1
    B[3:4, 1:7] = 1

    B[7:11, 11] = 1
    B[7:11, 14] = 1
    B[10:15, 10:15] = 1

    B[5:10, 5] = 1
    B[5:10, 6] = 1

    LB = two_pass_labeling(B)
    print("Labels - ", list(set(LB.ravel()))[1:])

    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(B, cmap="hot")
    plt.colorbar(ticks=range(int(2)))
    plt.axis("off")
    plt.subplot(122)
    plt.imshow(LB.astype("uint8"), cmap="hot")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()
    plt.show()