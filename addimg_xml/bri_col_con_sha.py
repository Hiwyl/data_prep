# -*- coding: utf-8 -*-
"""
@Author :       wyl
@Email :  wangyl306@163.com
@Date :      2020/5/14
"""

import os
import shutil
from PIL import Image
from PIL import ImageEnhance
from tqdm import tqdm

# 原始图像
def ImageAugument():
    imgs_save_dir = 'data/other_imgs/'
    if not os.path.exists(imgs_save_dir):
        os.makedirs(imgs_save_dir)
    xmls_save_dir = 'data/other_xmls/'
    if not os.path.exists(xmls_save_dir):
        os.makedirs(xmls_save_dir)
    path = "data/img"  # 文件夹目录
    xml_path="data/xml"
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    # 遍历文件夹
    prefix = path + '/'
    print("begin>>>")
    for file in tqdm(files):
        image = Image.open(prefix + file)
        xml=xml_path+"/"+file[:-4]+".xml"
       # image.show()

        # 亮度增强
        enh_bri = ImageEnhance.Brightness(image)
        brightness = 0.9
        image_brightened = enh_bri.enhance(brightness)
        image_brightened.save(imgs_save_dir + file[:-4] + 'lig' + '.jpg')
        new_name = xmls_save_dir+"/"+file[:-4]+"lig"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)

        # # 色度增强
        enh_col = ImageEnhance.Color(image)
        color = 1.5
        image_colored = enh_col.enhance(color)
        image_colored.save(imgs_save_dir + file[:-4] + 'col' + '.jpg')
        new_name = xmls_save_dir+"/"+file[:-4]+"col"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)

        # 对比度增强
        enh_con = ImageEnhance.Contrast(image)
        contrast = 1.5
        image_contrasted = enh_con.enhance(contrast)
        image_contrasted.save(imgs_save_dir + file[:-4] + 'con' + '.jpg')
        new_name = xmls_save_dir+"/"+file[:-4]+"con"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)

        # 锐度增强
        enh_sha = ImageEnhance.Sharpness(image)
        sharpness = 1.5
        image_sharped = enh_sha.enhance(sharpness)
        image_sharped.save(imgs_save_dir + file[:-4] + 'mor' + '.jpg')
        new_name = xmls_save_dir+"/"+file[:-4]+"mor"+".xml" # 为文件赋予新名字
        shutil.copyfile(xml, new_name)

    print("Done")

if __name__ == '__main__':
    ImageAugument()