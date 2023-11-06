import cv2
import numpy as np
import torch


from huakuang import detail_frame
from Unet import *

device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = '../CrackForest-dataset-master/save_model_dir/faker120A.pt'
unet = Unet().to(device)
model_dict = unet.load_state_dict(torch.load(model_path))
import win32api
import win32con
def cap_detail(img,unet):

    image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (320, 480))
    orgin_img=cv2.resize(img,(320,480))
    h, w = image.shape
    img = np.float32(image) / 255.0
    img = np.expand_dims(img, 0)
    x_input = torch.from_numpy(img).view(1, 1, h, w)

    probs = unet(x_input.to(device))

    m_label_out_ = probs.transpose(1, 3).transpose(1, 2).contiguous().view(-1, 2)
    grad, output = m_label_out_.data.max(dim=1)
    output[output > 0] = 255

    predic_ = output.view(h, w).cpu().detach().numpy()  # 得到的灰度图

    # 保存
    result = cv2.resize(np.uint8(predic_), (w, h))
    cv2.imwrite('07_result.jpg', result)

    result_img = cv2.imread('07_result.jpg')
    kernel = np.ones((2, 2), np.uint8)
    result_f = cv2.morphologyEx(result_img, cv2.MORPH_OPEN, kernel, iterations=2)

    # #画框展示
    detail_frame(orgin_img,result_f)

def cap(flag):
    if flag==0:
        capture = cv2.VideoCapture(0)
    else:#不是0，此时输入的是视频路径
        capture = cv2.VideoCapture(flag)
    ret = True
    while ret:
        # ret：是否有下一帧
        # frame：当前帧的ndarray
        ret, frame = capture.read()
        if ret:
            pass
        else:
            break
        cap_detail(frame, unet)
        key = cv2.waitKey(10)
        # 如果按下q键
        if key == ord('q'):
            break
    win32api.MessageBox(0, "播放结束！即将关闭", '提示', win32con.MB_OK)
    cv2.destroyWindow('Orgin')
    cv2.destroyWindow('Result')

