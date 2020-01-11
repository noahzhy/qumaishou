import os
import glob
import random
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def load_img():
    random.random()
    img_list = glob.glob('img_fusion/test/*')
    return random.choice(img_list)
    # return r'img_fusion\test\10002295747_03.jpg'


def img_fusion():
    img = cv2.imread(load_img())
    img = cv2.resize(img, (320, 320))
    # img_hsv = cv2.cvtColor(img, cv2.cvtColor)
    # cv2.imshow('original img', img)
    # img = subimage(img, [240, 240], 0, 480, 480)
    cv2.imshow('original img', img)
    # 获取mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([-1, -1, -1])
    upper_white = np.array([248,248,248])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # mask = cv2.GaussianBlur(mask, (3,3), 0)
    cv2.imshow('Mask', mask)
    # erode = cv2.erode(mask, None, iterations=1)
    # dilate = cv2.dilate(erode, None, iterations=1)
    # cv2.imshow('final', dilate)

    cv2.waitKey()
    # pass


def subimage(image, center, theta, width, height):
    theta *= np.pi / 180 # convert to rad

    v_x = (np.cos(theta), np.sin(theta))
    v_y = (-np.sin(theta), np.cos(theta))
    s_x = center[0] - v_x[0] * (width / 2) - v_y[0] * (height / 2)
    s_y = center[1] - v_x[1] * (width / 2) - v_y[1] * (height / 2)

    mapping = np.array([[v_x[0],v_y[0], s_x],
                        [v_x[1],v_y[1], s_y]])

    return cv2.warpAffine(image,mapping,(width, height),flags=cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)


def test():
    # Read image
    im_in = cv2.imread(load_img(), cv2.IMREAD_GRAYSCALE)
    im_in = cv2.resize(im_in, (320, 320))
    
    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    
    th, im_th = cv2.threshold(im_in, 227, 255, cv2.THRESH_BINARY_INV)
    
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
    
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    # Display images.
    cv2.imshow("original Image", im_in)
    # cv2.imshow("Floodfilled Image", im_floodfill)
    # cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
    cv2.imshow("Foreground", im_out)
    cv2.waitKey(0)
    pass


if __name__ == "__main__":
    # print([255*3])
    # img_fusion()
    test()