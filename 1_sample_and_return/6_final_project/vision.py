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
        warped = cv2.warpPerspective(img, self.perspective_matrix, (img.shape[1], img.shape[0]))
        warped[0:img.shape[0] // 3, :] = 0
        warped[:, :img.shape[1] // 5] = 0
        warped[:, -img.shape[1] // 5:] = 0
        return warped

    def process(self, img):
        rock = self.perspective_transform(self.low_threshold(img, (10, 30, 30)))
        navigable = self.high_threshold(img, (160, 160, 160))
        obstacle = self.perspective_transform(1 - navigable)
        navigable = self.perspective_transform(navigable)
        return obstacle, rock, navigable
