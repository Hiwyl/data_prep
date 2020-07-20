# -*- coding: utf-8 -*-
"""
@author:      wyl
@email: wangyl306@163.com
@data: Thu Jul  2 11:26:42 2020

albumentations方案
像素级转换
pip install albumentations
可定制化加入增强方案：https://github.com/albumentations-team/albumentations
"""
import cv2
from matplotlib import pyplot as plt
from tqdm import tqdm
import os
import shutil


from albumentations import (Blur, OpticalDistortion, GridDistortion, HueSaturationValue,
    IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, MedianBlur, RandomBrightnessContrast, RandomRain,RandomFog,RandomSunFlare,RandomShadow,RandomSnow,CoarseDropout,Cutout
)


def  augment_and_show(aug, image):
    plt.figure(figsize=(40,40))
    plt.subplot(2,1,1)
    plt.imshow(image)
    image1 = aug(image=image)['image']
    plt.subplot(2, 1, 2)
    plt.imshow(image1)
    plt.show()
# aug = RandomBrightnessContrast(brightness_limit=(0.1, 0.2),contrast_limit=(0.1, 0.2),p=1)
# aug =MedianBlur(blur_limit=3,p=1)


# 原始图像
def ImageAugument():
    imgs_save_dir = 'data/albu_imgs/'
    if not os.path.exists(imgs_save_dir):
        os.makedirs(imgs_save_dir)
    xmls_save_dir = 'data/albu_xmls/'
    if not os.path.exists(xmls_save_dir):
        os.makedirs(xmls_save_dir)
    path = "data/img"  # 文件夹目录
    xml_path="data/xml"
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    # 遍历文件夹
    prefix = path + '/'
    print("begin>>>")
    for file in tqdm(files):
        image=cv2.imread(prefix + file)
        # cv2.imwrite("origin.jpg",image)
        xml=xml_path+"/"+file[:-4]+".xml"

        #示例：使用具有随机孔径线性大小的中值滤波器来模糊输入图像
        aug =MedianBlur(p=1)
        
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'mb' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"mb"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #随机大小的内核模糊输入图像
        aug =Blur(p=1)
        
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'blur' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"blur"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #高斯模糊
        aug =GaussNoise(p=1)
        
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'gau' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"gau"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #随机雨
        aug =RandomRain(p=1)
        
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'rain' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"rain"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #随机雾
        aug =RandomFog(fog_coef_lower = 0.2,fog_coef_upper =0.5,alpha_coef = 0.1,p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'fog' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"fog"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #太阳耀斑RandomSunFlare
        aug =RandomSunFlare(p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'sun' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"sun"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #阴影RandomShadow
        aug =RandomShadow(p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'shadow' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"shadow"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #随机雪RandomSnow
        aug =RandomSnow(p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'snow' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"snow"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)
        
        #随机CoarseDropout
        aug =CoarseDropout(p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'drop' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"drop"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)        

        #随机cutout
        aug =Cutout(p=1)
         
        aug_image = aug(image=image)['image']
        cv2.imwrite(imgs_save_dir + file[:-4] + 'cut' + '.jpg',aug_image)
        new_name = xmls_save_dir+"/"+file[:-4]+"cut"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)    
        
    print("Done")

if __name__ == '__main__':
    ImageAugument()