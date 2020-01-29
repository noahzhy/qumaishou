__Author__ = 'Shliang'
import numpy as np
import cv2 as cv


def generate_trimap(alpha, write_name):
    
    # img = alpha
    
    # # 将图片转换到灰度空间
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # # 图像平滑
    # blur = cv.blur(gray, (3, 3))
    # ret, thresh = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)
    # alpha = thresh
    # alpha = cv.resize(alpha, (320,320))
    
    # cv.imshow('alpha', alpha)
    # cv.waitKey()

    # fg = np.array(np.less_equal(alpha, 240).astype(np.float32))
    # img = cv.resize(fg, (512, 512))
    # cv.imshow("fg", fg)
    # cv.waitKey(0)
    # fg = cv.erode(fg, kernel, iterations=np.random.randint(1, 3))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    unknown = np.array(np.less_equal(alpha, 220).astype(np.float32))

    unknown_dilate = cv.dilate(unknown, kernel, iterations=30)
    trimap = (unknown_dilate - unknown) * 127 + unknown * 255
    cv.imwrite("{}.png".format(write_name), trimap)

    return trimap.astype(np.uint8)


if __name__ == "__main__":
    # alpha = cv.imread(r"img_fusion\test\10002212732_01.jpg")
    img_src = r"img_fusion\test\10002336065_01.jpg"
    img_src = r'img_fusion\test\20000758013_1.jpg'
    alpha = cv.imread(img_src)
    img = generate_trimap(alpha, img_src.split('\\')[-1].split('.')[0])
    # cv.imread(img)
    img = cv.resize(img, (512, 512))
    cv.imshow("trimp", img)
    cv.waitKey(0)

    