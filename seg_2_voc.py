# -*- coding: utf-8 -*-
"""
@Author :       wyl
@Email :  wangyl306@163.com
@Time  :   2019/1/18 15:25
@Project : 11-安全带
@FileName:  seg_2_voc.py
"""
import os
import random
import numpy as np
import codecs
import json
from glob import glob
import cv2
import shutil
from sklearn.model_selection import train_test_split

# 1.标签路径
labelme_path = "/home/yongle.wang/projects/data_prep/data/train/"  # 原始labelme标注数据路径
saved_path = "/home/yongle.wang/projects/data_prep/data/"  # 保存路径
trainval_percent = 0.1
train_percent = 0.9

# 2.创建要求文件夹
if not os.path.exists(saved_path + "Annotations"):
    os.makedirs(saved_path + "Annotations")
if not os.path.exists(saved_path + "JPEGImages/"):
    os.makedirs(saved_path + "JPEGImages/")
if not os.path.exists(saved_path + "ImageSets/Main/"):
    os.makedirs(saved_path + "ImageSets/Main/")

# 3.获取待处理文件
files = glob(labelme_path + "*.json")
print(files)
files = [i.split("/")[-1].split(".json")[0] for i in files]
# 4.读取标注信息并写入 xml
for json_file_ in files:
    json_filename = labelme_path + json_file_ + ".json"
    json_file = json.load(open(json_filename, "r", encoding="utf-8"))
    try:
        height, width, channels = cv2.imread(labelme_path + json_file_ + ".jpg").shape
    except:
        print("+++++++++++++++++++ERROR++++++++++++++++++++")
    with codecs.open(saved_path + "Annotations/" + json_file_ + ".xml", "w", "utf-8") as xml:
        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'UAV_data' + '</folder>\n')
        xml.write('\t<filename>' + json_file_ + ".jpg" + '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database>The UAV autolanding</database>\n')
        xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
        xml.write('\t\t<image>flickr</image>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t</source>\n')
        xml.write('\t<owner>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t\t<name>ChaojieZhu</name>\n')
        xml.write('\t</owner>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>' + str(width) + '</width>\n')
        xml.write('\t\t<height>' + str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>0</segmented>\n')
        for multi in json_file["shapes"]:
            points = np.array(multi["points"])
            xmin = int(min(points[:, 0]))
            xmax = int(max(points[:, 0]))
            ymin = int(min(points[:, 1]))
            ymax = int(max(points[:, 1]))
            label = multi["label"]
            if xmax <= xmin:
                pass
            elif ymax <= ymin:
                pass
            else:
                xml.write('\t<object>\n')
                xml.write('\t\t<name>' + label + '</name>\n')
                xml.write('\t\t<pose>Unspecified</pose>\n')
                xml.write('\t\t<truncated>1</truncated>\n')
                xml.write('\t\t<difficult>0</difficult>\n')
                xml.write('\t\t<bndbox>\n')
                xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                xml.write('\t\t</bndbox>\n')
                xml.write('\t</object>\n')
                # print(json_filename, xmin, ymin, xmax, ymax, label)
        xml.write('</annotation>')
# 5.复制图片到 VOC2007/JPEGImages/下
image_files = glob(labelme_path + "*.jpg")
for image in image_files:
    shutil.copy(image, saved_path + "JPEGImages/")
print("copy %d images files to VOC007/JPEGImages/"%len(image_files))
# 6.split files for txt
xmlfilepath = saved_path +'Annotations'
txtsavepath = saved_path + "ImageSets/Main/"
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(txtsavepath+'trainval.txt', 'w')
ftest = open(txtsavepath+'test.txt', 'w')
ftrain = open(txtsavepath+'train.txt', 'w')
fval = open(txtsavepath+'val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        fval.write(name)
        ftest.write('\n')
        #if i in train:
            #fval.write(name)
        #else:
            #ftest.write(name)
    else:
        ftrain.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()