from skimage import data, exposure
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
from skimage import util
from skimage.exposure import histogram
import numpy as np


def reverse_img(img_loc):
    """
    Take address of image to be processed as img_loc.
    Computes log correction and returns both the input img and corrected img.

    param:
    img_loc - address to access image to be processed

    returns:
    img - 2D array of input image
    log_img - 2D array of log corrected image
    """
    img = imread(img_loc)
    reverse_img = np.asarray(util.invert(img), dtype='uint8')
    return img, reverse_img


# pull out RGB values for histogram
def RGB(img):
    """
    Takes img as np.array. Seperates rgb values and returns 3 arrays.

    params:
    img - array of image after performing imread

    returns:
    r, g, b - arrays of values for each color
    """
    img_shape = img.shape
    r = []
    g = []
    b = []
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            r.append(img[i, j, 0])
            g.append(img[i, j, 1])
            b.append(img[i, j, 2])
    return r, g, b

if __name__ == "__main__":
    img, reverse_img = reverse_img('image_0004.jpg')
    r, g, b = RGB(img)
    print('dis dah data')
    print(len(r))
    plt.figure(1)
    subplot(311)
    hist(r, 256, range=(0, 256), color = 'red')
    title('Red')
    subplot(312)
    hist(g, 256, range=(0, 256), color = 'green')
    title('Green')
    subplot(313)
    hist(b, 256, range=(0, 256), color = 'blue')
    title('Blue')
    plt.show()
    fig.tight_layout()
    # plt.imsave('reversed_image.tiff', reverse_img)
    # fig = plt.figure(figsize=(8, 5))
    # subplot(221)
    # imshow(img, cmap=get_cmap('gray'))
    # title('Original')
    # subplot(222)
    # hist(img.flatten(), 256, range=(0, 256))
    # title('Histogram of original')
    # subplot(223)
    # imshow(reverse_img, cmap=get_cmap('gray'))
    # title('Log Corrected')
    # subplot(224)
    # hist(reverse_img.flatten(), 256, range=(0, 256))
    # title('Histogram of Log Corrected')
    # fig.tight_layout()
    # show()