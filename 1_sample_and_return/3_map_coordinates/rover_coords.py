import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from extra_functions import perspect_transform, color_thresh, source, destination

image = mpimg.imread('../1_color_threshold/sample.jpg')


def rover_coords(binary_img):
    # Calculate pixel positions with reference to the rover
    # position being at the center bottom of the image.
    ypos, xpos = binary_img.nonzero()

    w, h, _ = image.shape
    x_pixel = -ypos + w
    y_pixel = -xpos + h / 2
    return x_pixel, y_pixel

# Perform warping and color thresholding
warped = perspect_transform(image, source, destination)
colorsel = color_thresh(warped, rgb_thresh=(160, 160, 160))
# Extract x and y positions of navigable terrain pixels
# and convert to rover coordinates
xpix, ypix = rover_coords(colorsel)

# Plot the map in rover-centric coords
fig = plt.figure(figsize=(5, 7.5))
plt.plot(xpix, ypix, '.')
plt.ylim(-160, 160)
plt.xlim(0, 160)
plt.title('Rover-Centric Map', fontsize=20)
plt.show()
