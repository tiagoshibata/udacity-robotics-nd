import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


def perspect_transform(img, src, dst):
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    return warped

source = np.float32([[14.4, 140.1], [118, 95.9], [199.5, 95.5], [301.8, 140]])
destination = np.float32([[30, 30], [30, 40], [40, 40], [40, 30]])

image = mpimg.imread('example_grid1.jpg')
warped = perspect_transform(image, source, destination)
plt.imshow(warped)
plt.show()
