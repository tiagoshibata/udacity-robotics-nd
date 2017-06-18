import cv2


img = cv2.imread('rock.png')
low = (110, 110, 110)
high = (10, 80, 80)
under_thresh = (img[:, :, 0] < low[0]) & (img[:, :, 1] < low[1]) & (img[:, :, 2] < low[2])
above_thresh = (img[:, :, 0] > high[0]) & (img[:, :, 1] > high[1]) & (img[:, :, 2] > high[2])
img[under_thresh] = 0
img[above_thresh] = 0
cv2.imshow('Rock', img)
while True:
    cv2.waitKey(0)
