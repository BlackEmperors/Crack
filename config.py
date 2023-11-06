
#数据处理mat
file_path='./CrackForest-dataset-master/groundTruth/'#mat文件
png_img_dir='./CrackForest-dataset-master/groundTruthPngImg'#处理后的mask文件夹

#数据路径
image_dir = './CrackForest-dataset-master/image/'
mask_dir = './CrackForest-dataset-master/groundTruthPngImg/'

#训练文本
epochs=100
train_on_gpu=True


model_path='./CrackForest-dataset-master/save_model_dir/unet_road_model.pt'
