from os.path import isdir
from scipy import io
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from config import *
if __name__ == '__main__':

    if not isdir(png_img_dir): #没有目录则创建
        os.mkdirs(png_img_dir)
    imgage_path_lists=os.listdir(file_path) #将所有的文件名放进一个列表里,便于使用序号区分
    # print(imgage_path_lists)
    images_path=[] #到时候一个一个的放入路径

    for index in range(len(imgage_path_lists)):
        image_file=os.path.join(file_path,imgage_path_lists[index])#这是想要转换的文件路径
        # print(image_file)
        images_path.append(image_file)
        image_mat=io.loadmat(image_file)#解读每一个mat文件放入这个变量里
        segmentation_image = image_mat['groundTruth']['Segmentation'][0] #寻找分割 'groundTruth': array([[(array([[1, 1, 1, 其实就是提取图片矩阵出来
        segmentation_image_array = np.array(segmentation_image[0])  #分割之后的图像阵列使用np处理,解析获得矩阵
        image = Image.fromarray((segmentation_image_array - 1) * 255) #转换为图像

        png_image_path = os.path.join(png_img_dir, "%s.png" % imgage_path_lists[index][0:3])#转换出保存图像的路径
        # print(png_image_path)
        image.save(png_image_path)
        plt.figure()
        plt.imshow(image)
        plt.pause(0.001)







