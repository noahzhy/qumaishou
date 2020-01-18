__Author__ = 'Shliang'
import numpy as np
import cv2 as cv


def generate_trimap(alpha):
    fg = np.array(np.equal(alpha, 255).astype(np.float32))
    # fg = cv.erode(fg, kernel, iterations=np.random.randint(1, 3))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    unknown = np.array(np.not_equal(alpha, 0).astype(np.float32))
    unknown = cv.dilate(unknown, kernel, iterations=np.random.randint(1, 20))
    trimap = fg * 255 + (unknown - fg) * 128
    cv.imwrite("trimp.jpg", trimap)
    return trimap.astype(np.uint8)


if __name__ == "__main__":
    alpha = cv.imread("/home/noah/qumaishou/img_fusion/test/10001852337_6.jpg")
    generate_trimap(alpha)