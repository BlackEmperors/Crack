import torch

#自己文件
from config import *
from dataset import *
from unet_plus import *
device="cuda" if torch.cuda.is_available() else "cpu"
#读取数据
dataloader = SegmentationDataset(image_dir, mask_dir)
train_loader = DataLoader(dataloader, batch_size=4, shuffle=False)
print("样本数量:", dataloader.num_of_samples(), len(dataloader), train_loader.dataset)
import tqdm
if __name__ == '__main__':
    index=0
    unet=NestedUNet().to(device)#加载unet网络
    optimizer=torch.optim.SGD(unet.parameters(),lr=0.01,momentum=0.9) #使用随机快速梯度下降算法
    for epoch in range(epochs):#开始每轮的训练
        train_loss=0.0 #看损失
        for i_batch,sample_batch in enumerate(train_loader): #获取对应的数据路径
            images_batch,target_labels=sample_batch['image'],sample_batch['mask'] #放入变量

            if train_on_gpu:
                images_batch, target_labels = images_batch.to(device), target_labels.to(device)
            optimizer.zero_grad()#把梯度置零,因为torch会累计而不是重置

            #开始进行前向算法
            m_label_out_ = unet(images_batch)#将图片放入
            # 计算损失值
            target_labels = target_labels.contiguous().view(-1)  # 执行contiguous()这个函数，把tensor变成在内存中连续分布的形式
            m_label_out_ = m_label_out_.transpose(1, 3).transpose(1, 2).contiguous().view(-1)
            target_labels = target_labels.long()
            loss = torch.nn.functional.cross_entropy(m_label_out_, target_labels)
            # print(loss)
            #后向传播 计算与模型参数有关的损失梯度
            loss.backward()
            # 参数更新
            optimizer.step()
            # 更新损失
            train_loss += loss.item()
            if index % 100 == 0:
                print('step: {} \tcurrent Loss: {:.6f} '.format(index, loss.item()))
            index += 1
        # 计算平均损失
        train_loss = train_loss / dataloader.num_of_samples()
        # 显示训练集与验证集的损失函数
        print('Epoch: {} \tTraining Loss: {:.6f} '.format(epoch, train_loss))

    # save model
    unet.eval()
    torch.save(unet.state_dict(), './CrackForest-dataset-master/save_model_dir/unet_Plus_model.pt')













