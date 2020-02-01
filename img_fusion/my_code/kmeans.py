import numpy as np
from PIL import Image as image
from sklearn.cluster import KMeans


def loadData(filePath):
    f = open(filePath, 'rb') #以二进制形式打开文件
    data = []
    img = image.open(f)
    m,n = img.size
    for i in range(m):
        for j in range(n):
            #将每个像素点RGB颜色处理到0-1范围内
            x,y,z =img.getpixel((i,j))
            #将颜色值存入data内
            data.append([x/256.0, y/256.0, z/256.0])
    f.close()
    #以矩阵的形式返回data，以及图片大小
    return np.mat(data), m, n

imgData, row, col = loadData(r'img_fusion\test\20000543988_1.jpg')#加载数据

km = KMeans(n_clusters=2)
#聚类获得每个像素所属的类别
label = km.fit_predict(imgData)
label = label.reshape([row, col])
#创建一张新的灰度图以保存聚类后的结果
pic_new = image.new("L", (row, col))
#根据类别向图片中添加灰度值
for i in range(row):
    for j in range(col):
        pic_new.putpixel((i, j), int(256/(label[i][j]+1)))
#以JPEG格式保存图像
pic_new.save("test.png", "PNG")