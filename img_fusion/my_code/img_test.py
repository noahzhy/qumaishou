__Author__ = 'Shliang'
import numpy as np
import cv2 as cv


def generate_trimap(alpha):
    fg = np.array(np.equal(alpha, 255).astype(np.float32))
    # fg = cv.erode(fg, kernel, iterations=np.random.randint(1, 3))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    unknown = np.array(np.not_equal(alpha, 255).astype(np.float32))

    unknown_dilate = cv.dilate(unknown, kernel, iterations=20)
    trimap = (unknown_dilate - unknown) * 128 + unknown *255
    cv.imwrite("trimp.png", trimap)

    return trimap.astype(np.uint8)


if __name__ == "__main__":
    alpha = cv.imread(r"img_fusion\test\10002212732_01.jpg")
    img = generate_trimap(alpha)
    # cv.imread(img)
    img = cv.resize(img, (512, 512))
    cv.imshow("trimp", img)
    cv.waitKey(0)

    