import numpy as np

structs = []
structs.append(np.array([[1, 1, 0, 0, 1, 1],
                         [1, 1, 0, 0, 1, 1],
                         [1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1]]))
structs.append(np.rot90(structs[-1]))
structs.append(np.rot90(structs[-1]))
structs.append(np.rot90(structs[-1]))
structs.append(np.array([[1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1]]))
structs.append(np.rot90(structs[-1]))


def calculate_count(img: np.ndarray, structs_: list):
    count = [0] * len(structs_)
    for i in range(img.shape[0]):

        for j in range(img.shape[1]):
            for z, struct in enumerate(structs_):
                w = struct.shape[0]
                h = struct.shape[1]
                if (i + w <= img.shape[0]) and (j + h <= img.shape[1]):
                    if (img[i:i + w, j:j + h] == struct).all():
                        print('+1')
                        count[z] += 1
    return count


if __name__ == '__main__':
    image = np.load("ps.npy").astype("uint8")
    counts = calculate_count(image, structs)
    for i in range(len(counts)):
        print(f"Type {i}: {counts[i]}")
