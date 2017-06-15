import cv2
import numpy as np


class Vision:
    def __init__(self):
        dst_size = 5
        bottom_offset = 6
        destination = np.float32([
            [160 - dst_size, 160 - bottom_offset],
            [160 + dst_size, 160 - bottom_offset],
            [160 + dst_size, 160 - 2 * dst_size - bottom_offset],
            [160 - dst_size, 160 - 2 * dst_size - bottom_offset],
        ])
        self.perspective_matrix = cv2.getPerspectiveTransform(
            np.float32([[14, 140], [301, 140], [200, 96], [118, 96]]),
            destination,
        )

    def binary_mask(self, img, mask):
        # Same size as img, but single channel
        filtered = np.zeros_like(img[:, :, 0])
        filtered[mask] = 1
        return filtered

    def high_threshold(self, img, thresh):
        above_thresh = (img[:, :, 0] > thresh[0]) & (img[:, :, 1] > thresh[1]) & (img[:, :, 2] > thresh[2])
        return self.binary_mask(img, above_thresh)

    def low_threshold(self, img, thresh):
        under_thresh = (img[:, :, 0] < thresh[0]) & (img[:, :, 1] < thresh[1]) & (img[:, :, 2] < thresh[2])
        return self.binary_mask(img, under_thresh)

    def perspective_transform(self, img):
        return cv2.warpPerspective(img, self.perspective_matrix, (img.shape[1], img.shape[0]))

    def process(self, img):
        obstacle = self.perspective_transform(self.low_threshold(img, (10, 10, 10)))
        rock = self.perspective_transform(self.low_threshold(img, (10, 30, 30)))
        navigable = self.perspective_transform(self.high_threshold(img, (160, 160, 160)))
        return obstacle, rock, navigable
