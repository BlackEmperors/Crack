

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from config import *
class SegmentationDataset(object):
    def __init__(self,image_dir,mask_dir):#input 路径
        self.images=[] #创立两个图片矩阵
        self.masks=[]
        files=os.listdir(image_dir) #两种文件来源
        sfiles=os.listdir(mask_dir)

        for i in range(len(sfiles)):#查看有多少mask进行处理
            img_file=os.path.join(image_dir,files[i])  #提取出文件
            mask_file = os.path.join(mask_dir, sfiles[i])
            # print(img_file,mask_file)
            self.images.append(img_file) #放入自身变量，便于后面处理
            self.masks.append(mask_file)
    def __len__(self):
        return len(self.images)
    def num_of_samples(self):
        return len(self.images)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx=idx.tolist() #将其转为列表
            image_path=self.images[idx]
            mask_path=self.masks[idx]
        else:
            image_path = self.images[idx]
            mask_path = self.masks[idx]
        img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)#得到灰度图片矩阵
        mask=cv2.imread(mask_path,cv2.IMREAD_GRAYSCALE)


        # print(img)
        #输入图像
        img=np.float32(img)/255.0 #把矩阵转换为图片
        img=np.expand_dims(img,0) #增加维度，灰度图片的层是320x480，现在是320x480x0
        #目标标签0~1，对于
        mask[mask<=128]=0 #取一半为标准。小于一般的都是 黑！！！
        mask[mask>128]=1#大于一半的都是白
        mask=np.expand_dims(mask,0) #与图片保存一致
        sample={'image':torch.from_numpy(img),'mask':torch.from_numpy(mask),}#样本变量里放入这个字典里,并且转换为torch类型数据
        return sample

def imshow_image(mydata_loader):
    plt.figure()
    for (cnt,i) in enumerate(mydata_loader):
        image=i['image']
        label=i['mask']
        for j in range(8):#一个批次为8
            ax1=plt.subplot(121)
            ax2 = plt.subplot(122)
            # permute函数：可以同时多次交换tensor的维度

            ax1.imshow(image[j].permute(1, 2, 0), cmap='gray')
            ax1.set_title('image')

            ax2.imshow(label[j].permute(1, 2, 0), cmap='gray')
            ax2.set_title('mask')
            # plt.pause(0.005)
            plt.show()
        if cnt == 6:
            break
        plt.pause(0.005)

if __name__ == '__main__':
    dataloader=SegmentationDataset(image_dir=image_dir,mask_dir=mask_dir)
    mydata_loader = DataLoader(dataloader, batch_size=8, shuffle=False)
    imshow_image(mydata_loader)
