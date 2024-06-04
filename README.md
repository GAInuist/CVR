# CVR 基于深度学习的虚拟图像到真实图像的转换
开发平台：Pycharm
环境需求：Linux、Python3、Anaconda虚拟环境配置工具、CPU or NVIDIA GPU + CuDNN
虚拟环境需要安装的软件包：
1.	Python==3.9
2.	numpy==1.24.2
3.	torchvision==0.8.2
4.	mpi4py（最好使用conda安装）
5.	pytorch-cuda==11.8(与cuda版本有关，这是cuda为11.8及以上版本)
6.	tqdm
7.	pandas==2.0.1
8.	Pillow==9.5.0
9.	opencv_python==4.7.0.72
10.	einops
11.	basicsr==1.3.4.9
12.	blobfile==2.1.1
13.	scipy
14.	PyQt5

注：虚拟环境创建指令为 conda create -name 自主命名环境 python==3.9

Segment Anything 原网址：https://github.com/facebookresearch/segment-anything

Semantic Image Synthesis via Diffusion Models(SDM) 原网址：https://github.com/WeilunWang/semantic-diffusion-model

HAT 原网址：https://github.com/XPixelGroup/HAT

文件结构
![b563ce9ce3c0f565661a3b7bb726b82](https://github.com/GAInuist/CVR/assets/157414652/917a99d6-26d2-4e4a-bb4f-fd5226a37ab5)

## 使用方式

下载模型权重文件到本地并将其放置到指定位置

语义分割模型下载点：


[(https://drive.google.com/file/d/1hN---Ii52UCNnihmC2YrqkxdlcEHfgTN/view)](https://drive.google.com/file/d/1hN---Ii52UCNnihmC2YrqkxdlcEHfgTN/view)


存放位置：CVR/SAM/experiment/model/semantic_sam/model.pth


语义合成模型下载点：

[https://drive.google.com/file/d/1NE3AiwsKl7l3TJyPCyxvysc7cxSttvM5/view](https://drive.google.com/file/d/1NE3AiwsKl7l3TJyPCyxvysc7cxSttvM5/view)


存放位置：CVR/SDM/OUTPUT/save/seas_256-300000-l1.pt

超分模型下载点：


[HAT_SRx4_ImageNet-pretrain.pth - Google 云端硬盘](https://drive.google.com/file/d/1NKYfmexIQ3gXe3Td3ef5jXHXUGxJBJkg/view)


存放位置：CVR/HAT-main/model/HAT_SRx4_ImageNet-pretrain.pth

本文件中已将三个模型的执行过程通过终端指令调用的方式进行集成，可以直接通过运行UI.py文件进行调用，下面将讲解一些使用时可以按照实际需要更改的地方。

## 主界面：

![image](https://github.com/GAInuist/CVR/assets/157414652/2cd4fd43-d11c-41ad-b01f-97eb5161dc09)

UI界面中可以选择图像生成、语义分割、语义合成以及超分辨率化四种操作类型。
选择图像生成即为将虚拟图像作为输入生成真实图像；
语义分割、语义合成以及超分辨率化为三个阶段的子任务。
	使用时只需选择输入文件的文件夹即可。

每个操作类型的输入图片文件夹选择说明：
1、	图像生成：存放虚拟图像的文件夹
2、	语义分割：存放虚拟图像的文件夹
3、	语义合成：选择的文件夹内需存放images/validation和annotations/validation两种文件，images/validation中存放原始虚拟图像，annotations/validation存放原始虚拟图像对应的分割图像
4、	超分辨率化：任意存放需要超分的图像的文件夹

各阶段任务的生成结果存放位置：
	语义分割的生成结果所在位置：CVR/dataset/Sea/annotations/validation/
	语义合成的生成结果所在位置：CVR/output/samples/
	超分辨率化的生成结果所在位置：CVR/HAT-main/results/HAT_SRx4_ImageNet-LR/visualization/custom/

Pytorch-cuda的下载方式：
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

## 可能遇到的问题：

1.运行SAM中的predict.py时如出现以下情况：

 ![image](https://github.com/GAInuist/CVR/assets/157414652/065959af-aae8-4c0e-ac23-ce4f2ef55fb3)

将下面红框位置删除即可：

 ![image](https://github.com/GAInuist/CVR/assets/157414652/1684c29a-a629-48a8-b8c8-a1e399f1ff6e)

2.安装basicsr包时如出现以下情况：

 ![image](https://github.com/GAInuist/CVR/assets/157414652/6d12ef3e-5982-4322-9d05-6ebdda8f35bd)

安装cython包后再安装basicsr包

如果安装时还遇到类似以下情况时，安装好红框位置的包即可：

 ![image](https://github.com/GAInuist/CVR/assets/157414652/e2c52579-6f93-48f7-99b1-669a8efb111b)

安装basicsr包前还得安装tb-nightly包：

pip install -i https://mirrors.aliyun.com/pypi/simple tb-nightly

上述情况都满足之后安装basicsr包才能成功。

3.安装PyQt5后运行UI.py时如果出现以下情况：

 ![image](https://github.com/GAInuist/CVR/assets/157414652/f853ee75-9a4e-47c1-b522-1242d2326125)

安装丢失依赖：

sudo apt-get update

sudo apt-get install libx11-xcb1 libxcb1 libxcb-util1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 
libxcb-shm0 libxcb-sync1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0

