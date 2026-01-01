import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from tqdm import tqdm

x_max, x_min = 2, -2
y_max, y_min = 2, -2


def heat_map(size, datafile):
    img = np.zeros((size, size), dtype=np.float32)

    roots = np.load(datafile, mmap_mode='r')

    for root in tqdm(roots, unit=' roots'):
        px = int((size - 1) * (root.real - x_min) / (x_max - x_min))
        py = int((size - 1) * (root.imag - y_min) / (y_max - y_min))

        if 0 <= px < size and 0 <= py < size:
            img[py, px] += 1.0

    nonzero = img > 0
    img[nonzero] = np.log(img[nonzero])
    img /= img.max()

    return img


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', type=int, default=2000,
                        help='image size in pixels')
    parser.add_argument('data', type=str,
                        help='roots data file')
    parser.add_argument('-o', type=str, default='polyroots.png',
                        help='output filename')
    parser.add_argument('-d', type=int, default=300,
                        help='dpi')
    args = parser.parse_args()

    img = heat_map(args.s, args.data)

    fig = plt.figure(figsize=(args.s / args.d, args.s / args.d),
                     dpi=args.d)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(img, cmap='afmhot')

    fig.savefig(args.o, dpi=args.d, bbox_inches='tight', pad_inches=0)
    plt.close(fig)


if __name__ == '__main__':
    main()
