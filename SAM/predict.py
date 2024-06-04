import numpy as np
import torch
import cv2
from torchvision import transforms
from torch import nn as nn
import os
from PIL import Image
import argparse

# os.environ["CUDA_VISIBLE_DEVICES"] = '0'

# img_path = r'../CVR/dataset/Sea/images/validation'
# output_gray_path = r'../CVR/dataset/Sea/annotations/validation'  # 输出路径
# model_pth = r'/media/c402/Windows/LF/finetune-anything-main/sam_ckpt/sam_FA_torcs.pth'
model_pth = r'../CVR/SAM/experiment/model/semantic_sam/model.pth'
# model_pth = r'experiment/model/semantic_sam/model.pth'

# 使用argparse解析命令行参数
parser = argparse.ArgumentParser(description='Process some paths and settings.')
parser.add_argument('--cuda_visible_devices', type=str, default='0', help='CUDA visible devices')
parser.add_argument('--img_path', type=str, required=True, help='Path to input images')
parser.add_argument('--output_gray_path', type=str, default='./dataset/Sea/annotations/validation', help='Path to save output grayscale images')
args = parser.parse_args()

# 设置CUDA_VISIBLE_DEVICES环境变量
os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_visible_devices

# 获取参数
img_path = args.img_path
output_gray_path = args.output_gray_path

# model_pth = args.model_pth


to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((1024, 1024))
])


model = torch.load(model_pth)
data = os.listdir(img_path)
for index in data:
    image_name = index.split('.')[0] + '.jpg'
    image_path = os.path.join(img_path, image_name)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = to_tensor(image).unsqueeze(0).to('cuda:0')
    # print(img.shape)
    mask, _ = model(img)  # 模型输出mask和iou
    prediction = torch.argmax(mask, dim=1).squeeze().detach().cpu().numpy()
    # print(np.unique(prediction))
    print('now is {} image for gray,image_name is {}'.format(index, image_name))
    prediction = np.asarray(np.uint8(prediction))
    # print(np.unique(prediction))
    # print(prediction.shape)

    image = Image.fromarray(prediction)
    image.save(os.path.join(output_gray_path, image_name.split('.')[0] + '.png'))
