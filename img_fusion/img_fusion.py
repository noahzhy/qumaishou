import os
import glob
import random
import cv2
import numpy as np
from PIL import Image



def load_img():
    img_list = glob.glob('img_fusion/test/*')
    return random.choice(img_list)


def img_fusion():
    img = cv2.imread(load_img())
    img = cv2.resize(img, (320, 320))
    cv2.imshow('original img', img)
    cv2.waitKey()
    # pass


if __name__ == "__main__":
    img_fusion()