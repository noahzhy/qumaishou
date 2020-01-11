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
    upper_white = np.array([240,240,240])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # mask = cv2.GaussianBlur(mask, (3,3), 0)
    cv2.imshow('Mask', mask)
    # erode = cv2.erode(mask, None, iterations=1)
    # dilate = cv2.dilate(erode, None, iterations=1)
    # cv2.imshow('final', dilate)

    sub_img = cv2.bitwise_or(img, img, mask=mask)
    cv2.imshow('mask', sub_img)

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


def test(resize=500):
    # Read image
    img = cv2.imread(load_img())
    img = cv2.resize(img, (resize, resize))
    im_in = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    
    th, im_th = cv2.threshold(im_in, 245, 255, cv2.THRESH_BINARY_INV)
    
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
    cv2.imshow("original Image", img)
    # cv2.imshow("Floodfilled Image", im_floodfill)
    # cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
    cv2.imshow("Foreground", im_out)

    # 过滤掉小的contours
    # 获取边缘信息
    contours, hierarchy = cv2.findContours(image=im_out,mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)


    def contours_area(cnt):
        # 计算countour的面积
        (x, y, w, h) = cv2.boundingRect(cnt)
        return w * h

    # 获取面积最大的contour
    max_cnt = max(contours, key=lambda cnt: contours_area(cnt))

    # 创建空白画布
    mask = np.zeros_like(im_out)
    # 获取面积最大的 contours
    mask = cv2.drawContours(mask,[max_cnt],0,255,-1)
    # 打印罩层
    # cv2.imshow('mask', mask)

    sub_img = cv2.bitwise_or(img, img, mask=mask)
    cv2.imshow('mask', sub_img)

    cv2.waitKey(0)
    pass


def test2():
    def get_holes(image, thresh):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
        im_bw_inv = cv2.bitwise_not(im_bw)

        contour, _ = cv2.findContours(im_bw_inv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            cv2.drawContours(im_bw_inv, [cnt], 0, 255, -1)

        nt = cv2.bitwise_not(im_bw)
        im_bw_inv = cv2.bitwise_or(im_bw_inv, nt)
        return im_bw_inv


    def remove_background(image, thresh, scale_factor=1, kernel_range=range(1, 3), border=None):
        border = border or kernel_range[-1]

        holes = get_holes(image, thresh)
        small = cv2.resize(holes, None, fx=scale_factor, fy=scale_factor)
        bordered = cv2.copyMakeBorder(small, border, border, border, border, cv2.BORDER_CONSTANT)

        for i in kernel_range:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*i+1, 2*i+1))
            bordered = cv2.morphologyEx(bordered, cv2.MORPH_CLOSE, kernel)

        unbordered = bordered[border: -border, border: -border]
        mask = cv2.resize(unbordered, (image.shape[1], image.shape[0]))
        fg = cv2.bitwise_and(image, image, mask=mask)
        return fg


    img = cv2.imread(load_img())
    nb_img = remove_background(img, 240)
    nb_img = cv2.resize(nb_img, (320, 320))
    cv2.imshow('mask', nb_img)
    cv2.waitKey()
    pass



if __name__ == "__main__":
    # print([255*3])
    # img_fusion()
    # test(500)
    test2()