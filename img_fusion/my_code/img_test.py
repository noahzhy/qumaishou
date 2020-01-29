__Author__ = 'Shliang'
import numpy as np
import cv2 as cv
import random
import glob


def generate_trimap(alpha, write_name):
    
    img = alpha
    
    # 将图片转换到灰度空间
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # 图像平滑
    blur = cv.blur(gray, (3, 3))
    ret, thresh = cv.threshold(blur, 240, 255, cv.THRESH_BINARY)
    alpha = thresh
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
    trimap = (unknown_dilate - unknown) * 128 + unknown * 255
    cv.imwrite("{}.png".format(write_name), trimap)

    return trimap.astype(np.uint8)


def gen_trimap(path):
    import numpy as np
    import cv2
    from matplotlib import pyplot as plt
    
    img = cv2.imread(path)
    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    rect = (50,50,450,290)

    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    plt.imshow(img)
    plt.colorbar()
    plt.show()


def load_img():
    random.random()
    img_list = glob.glob('img_fusion/test/*')
    img_path = random.choice(img_list)

    return img_path

if __name__ == "__main__":
    # alpha = cv.imread(r"img_fusion\test\10002212732_01.jpg")
    # img_src = load_img()
    # # img_src = r'img_fusion\test\20000758013_1.jpg'
    # alpha = cv.imread(img_src)
    # img = generate_trimap(alpha, img_src.split('\\')[-1].split('.')[0])
    # img = cv.resize(img, (512, 512))
    # cv.imshow("trimp", img)
    # cv.waitKey(0)
    gen_trimap(load_img())

    