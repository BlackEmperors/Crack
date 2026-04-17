import os

import win32api
import win32con
import wx

from video_inference import cap
from image_inference import img_detail
from config import *
from unet import *

#模型加载
device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = '../CrackForest-dataset-master/save_model_dir/BIG120A.pt'
unet = Unet().to(device)
model_dict = unet.load_state_dict(torch.load(model_path))

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None,title='道路裂缝检测系统',size=(840,480))
        self.Center()
        #Pannel画布 添加控件
        global mainPanel
        mainPanel=wx.Panel(self)
        self.addMainPanelChildren()

        mainPanel.Bind(wx.EVT_KEY_DOWN,self.choseecent)

    def addMainPanelChildren(self):
        wx.StaticText(mainPanel,label='  待机界面...')

        #先把要的东西准备好
        font_title=wx.Font(28, wx.MODERN, wx.NORMAL, wx.BOLD, False, 'myfont')
        txt_title=wx.StaticText(mainPanel,label='欢迎进入道路裂缝检测系统')
        txt_title.SetFont(font_title)
        txt_reminder=wx.StaticText(mainPanel,label='按任意键进入系统')

        #开始摆放
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(txt_title, proportion=3, flag=wx.CENTER | wx.TOP, border=100)
        vbox.Add(txt_reminder, proportion=1, flag=wx.CENTER)

        mainPanel.SetSizer(vbox)

    def choseecent(self, event):  # event 具体事件对象
        self.chosemain()
    def chosemain(self):
        # 清空当前界面所有的控件
        mainPanel.DestroyChildren()
        font_title = wx.Font(28, wx.MODERN, wx.NORMAL, wx.BOLD, False, 'myfont')
        txt_title = wx.StaticText(mainPanel, label='道路裂缝检测系统正在运行，请选择运行模式...')


        # 画四个button
        btn_image = wx.Button(mainPanel, label='图片检测', pos=(60, 330), size=(150, 60))
        btn_video = wx.Button(mainPanel, label='视频检测', pos=(250, 330), size=(150, 60))
        btn_cap = wx.Button(mainPanel, label='实时检测', pos=(440, 330), size=(150, 60))
        btn_back=wx.Button(mainPanel, label='退出检测', pos=(630, 330), size=(150, 60))

        #绑定各自的事件
        btn_image.Bind(wx.EVT_BUTTON, self.imagedetail)
        btn_video.Bind(wx.EVT_BUTTON, self.videodetail)
        btn_cap.Bind(wx.EVT_BUTTON, self .capdetail)
        btn_back.Bind(wx.EVT_BUTTON, self.cancelLogin)

        mainPanel.Layout()

    def imagedetail(self, event):
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select picture', os.getcwd(), '', wildcard, wx.FD_OPEN)  #####这个部分新旧版本有变化
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath().replace("\\", "/")
        if file_path.endswith('.jpg')|file_path.endswith('.jpeg')|file_path.endswith('.png'):
            win32api.MessageBox(0, "正在为您打开图片检测，请确定！", '提示', win32con.MB_OK)
            img_detail(file_path,unet)
        else:
            win32api.MessageBox(0, "您所选择的文件后缀不是jpg,jpeg或png,请重新尝试！",'提示', win32con.MB_OK)

    def videodetail(self, event):
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select video', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath().replace("\\", "/")
        if file_path.endswith('.mp4')|file_path.endswith('.avi')|file_path.endswith('.wmv'):
            win32api.MessageBox(0, "正在为您打开视频检测，请确定！(检测过程按下q可以退出)", '提示', win32con.MB_OK)
            cap(file_path)
        else:
            win32api.MessageBox(0, "您所选择的文件后缀不是.mp4,.avi或.wmv,请重新尝试！",'提示', win32con.MB_OK)


    def capdetail(self, event):
        win32api.MessageBox(0, "正在为您打开摄像头实时检测(检测过程按下q可以退出)，请确定！", '提示', win32con.MB_OK)
        try:
            cap(0)
        except Exception as e:
            win32api.MessageBox(0, "发生了错误请重试", '提示', win32con.MB_OK)
    def cancelLogin(self,event):
        mainPanel.DestroyChildren()    # 擦除 mainPanel 当前的所有控件
        self.addMainPanelChildren()
        mainPanel.Layout()      #  强迫  mainPanel 去重新计算 它里面的基础控件的位置

class App(wx.App):
    def OnInit(self):
        frame =MainWindow()
        frame.Show()

        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()