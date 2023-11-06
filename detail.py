import cv2
import numpy as np
import torch


from huakuang import detail_frame
from Unet import *

device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = './CrackForest-dataset-master/save_model_dir/faker120A.pt'
unet = Unet().to(device)
model_dict = unet.load_state_dict(torch.load(model_path))
def img_detail(img_path,unet):
    test_image=img_path
    begain_image=cv2.imread(test_image)
    begain_image = cv2.resize(begain_image,(320,480))#duoyu?
    image=cv2.imread(test_image,cv2.IMREAD_GRAYSCALE)
    image=cv2.resize(image,(320,480))#原图
    h,w=image.shape
    img=np.float32(image)/255.0#(480, 320)
    img=np.expand_dims(img,0) #在最外面加一个[](1, 480, 320)
    x_input=torch.from_numpy(img).view(1,1,h,w)#torch.Size([1, 1, 480, 320])

    probs=unet(x_input.to(device))#torch.Size([1, 2, 480, 320])


    m_label_out_ = probs.transpose(1, 3).transpose(1, 2).contiguous().view(-1, 2)#.13 torch.Size([1, 320, 480, 2]) .12 torch.Size([1, 480, 320, 2])
                                                                                 #.contiguous()是将数据独立出来,view-1自动分配维度，2为每行两个
    grad, output = m_label_out_.data.max(dim=1)#把数据里每一个较大大的提取出来，由于是二维数组，dim为0把每一列的最大值，dim为1则是找每一行的最大值
                                                #找两者最大值的原因是大的像素点就是得出的轮廓，小的像素点属于背景像素
    output[output > 0] = 255#将其变为255为白色

    predic_ = output.view(h, w).cpu().detach().numpy()#张量转换图片得到的灰度图




    # 保存
    result = cv2.resize(np.uint8(predic_), (w, h))
    cv2.imwrite('07_result.jpg', result)

    result_img=cv2.imread('07_result.jpg')
    kernel=np.ones((2,2),np.uint8)

    result_f=cv2.morphologyEx(result_img,cv2.MORPH_OPEN,kernel,iterations=2)

    cv2.imwrite('08_result.jpg', result_f)
    #画框展示
    # detail_frame(begain_image,result_f)

    a=cv2.imread('08_result.jpg')
    test=cv2.add(begain_image,a)
    cv2.imshow('test',test)
    cv2.waitKey(0)
#2x2 四次
#3x3 2次


if __name__ == '__main__':
    img_detail('F:/AI-pycharm/Crack/test/01.jpg',unet)