import cv2
import numpy as np
#
# img1=cv2.imread('./test/04.jpg')
# img1=cv2.resize(img1,(320,480))
# img2=cv2.imread('./04_result.jpg')

# 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
    # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
    # 明度（V），取0-100%。
    # OpenCV中H,S,V范围是0-180,0-255,0-255

def detail_frame(img1,img):#输入原图路径和二值图路径
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.
    low = np.array([0, 0, 221])
    high = np.array([180, 30, 255])
    dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域
    # 寻找白色的像素点坐标。
    # 白色像素值是255，所以np.where(dst==255)
    xy = np.column_stack(np.where(dst == 255))
    white_all=len(xy)#全部白点数量
    if white_all!=0:
        X = xy[:, 0]
        x_min = min(X)
        x_max = max(X)
        Y = xy[:, 1]
        y_min = min(Y)
        y_max = max(Y)
        # print(x_min, x_max, y_min, y_max)
        puttext='Crack'
    else:
        x_min = 0
        y_min = 40
        puttext='None'
    # 绘制
    cv2.imshow('Orgin', img1)
    if puttext=='Crack':
        cv2.rectangle(img1, (y_min, x_min), (y_max, x_max), (0, 255, 0), 5)
    cv2.putText(img1, puttext, (x_min, y_min), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), thickness=1)
    cv2.imshow('Result', img1)


#考虑自己的置信度
'''

（白点数量/全部白点数量） *（白点数量/相数数量）=（白点数量）^2/（全白点*像素数量）
起始画法包含为1，所以 后面应该为白点数量/像素数量

    #test
    best_iou=white_all/(len(X)*len(Y)) #一开始的iou 最好的是..
    #设置一个列表，依次放入像素点，然后进行判断是不是白色,第一个必定是白色
    test=[]
    xylist=xy.tolist()#将np转换为列表
    # print(xylist)

    # for i in range(x_min,x_max+1):#建立起列表组
    #     for j in range(y_min,y_max):
    #         #[x,y]坐标已经遍历出来了
    #         test.append([i,j])
    #
    # for i in range(0, len(test)):
    #     for j in range(i+1, len(test)):  # 从i开始算 本身是0.0到结尾
    #         white_now = 0
    #         new = test[i:j]
    #         for w in new:
    #             if w in new:
    #                 white_now += 1

            # now_iou=((white_now)*(white_now))/(white_all*len(new))
            # if now_iou>=best_iou:
            #     best_min=new[0]
            #     best_max=new[-1]
            print(best_iou)
'''





