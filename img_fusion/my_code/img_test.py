__Author__ = 'Shliang'
import numpy as np
import cv2 as cv
import random
import glob


def test2(path):
    def get_holes(image, thresh):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        im_bw = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)[1]
        im_bw_inv = cv.bitwise_not(im_bw)
        contour, _ = cv.findContours(im_bw_inv, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        
        for cnt in contour:
            cv.drawContours(im_bw_inv, [cnt], 0, 255, -1)

        nt = cv.bitwise_not(im_bw)
        im_bw_inv = cv.bitwise_or(im_bw_inv, nt)
        return im_bw_inv


    def remove_background(image, thresh, scale_factor=1, kernel_range=range(1, 3), border=None):
        border = border or kernel_range[-1]
        holes = get_holes(image, thresh)
        small = cv.resize(holes, None, fx=scale_factor, fy=scale_factor)
        bordered = cv.copyMakeBorder(small, border, border, border, border, cv.BORDER_CONSTANT)

        for i in kernel_range:
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2*i+1, 2*i+1))
            bordered = cv.morphologyEx(bordered, cv.MORPH_CLOSE, kernel)

        unbordered = bordered[border: -border, border: -border]
        mask = cv.resize(unbordered, (image.shape[1], image.shape[0]))
        fg = cv.bitwise_and(image, image, mask=mask)
        return fg

    img_path = path
    # img_name = img_path.split('\\')[-1]
    img = cv.imread(img_path)
    # img = cv.resize(img, (320, 320))
    # cv.imshow('org', img)
    nb_img = remove_background(img, 240)
    # nb_img = cv.resize(nb_img, (320, 320))
    # cv.imshow('mask', nb_img)
    # result_img = 'img_fusion/test_result/{}'.format(img_name)
    # result_img = result_img.replace('.jpg', '.png')
    # cv.imwrite(result_img, nb_img)
    # cv.waitKey()
    return nb_img


def generate_trimap(alpha, write_name):
    
    img = alpha
    
    # 将图片转换到灰度空间
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # 图像平滑
    blur = cv.blur(gray, (3, 3))
    ret, thresh = cv.threshold(blur, 0, 100, cv.THRESH_BINARY)
    alpha = thresh

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    unknown_dilate = cv.dilate(alpha, kernel, iterations=20)
    trimap = (unknown_dilate - alpha) * 128 + alpha * 255

    alpha = cv.resize(alpha, (720,720))
    cv.imshow('alpha', alpha)
    cv.waitKey()

    # fg = np.array(np.less_equal(alpha, 240).astype(np.float32))
    # img = cv.resize(fg, (512, 512))
    # cv.imshow("fg", fg)
    # cv.waitKey(0)
    # fg = cv.erode(fg, kernel, iterations=np.random.randint(1, 3))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    unknown = np.array(np.less_equal(alpha, 220).astype(np.float32))

    unknown_dilate = cv.dilate(unknown, kernel, iterations=30)
    trimap = (unknown_dilate - unknown) * 128 + unknown * 255
    cv.imwrite(r"E:\github_clone\indexnet_matting\examples\images\test_origin.png", img)
    cv.imwrite(r"E:\github_clone\indexnet_matting\examples\trimaps\test_trimap.png", trimap)

    return trimap.astype(np.uint8)


def load_img():
    random.random()
    img_list = glob.glob('img_fusion/test/*')
    img_path = random.choice(img_list)

    return img_path

if __name__ == "__main__":
    # alpha = cv.imread(r"img_fusion\test\10002212732_01.jpg")
    img_src = load_img()
    # # img_src = r'img_fusion\test\20000758013_1.jpg'
    # alpha = cv.imread(img_src)
    alpha = test2(img_src)
    img = generate_trimap(alpha, img_src.split('\\')[-1].split('.')[0])
    img = cv.resize(img, (512, 512))
    cv.imshow("trimp", img)
    cv.waitKey(0)
    # gen_trimap(load_img())

    