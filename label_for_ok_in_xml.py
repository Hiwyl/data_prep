# -*- coding: utf-8 -*-
"""
@Author :       wyl
@Email :  wangyl306@163.com
"""
import os
import cv2
import codecs

#图片路径
img_dir="data/test_ok"
saved_path="data/ok_xml"
if not os.path.exists(saved_path):
    os.makedirs(saved_path)
imgs=os.listdir(img_dir)
for img in imgs:
    height, width, channels = cv2.imread(img_dir+"/"+img).shape
    with codecs.open(saved_path +"/" +img.split(".")[0] + ".xml", "w", "utf-8") as xml:
        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'UAV_data' + '</folder>\n')
        xml.write('\t<filename>' + img+ '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database>ok</database>\n')
        xml.write('\t\t<annotation>by wyl</annotation>\n')
        xml.write('\t\t<image>flickr</image>\n')
        xml.write('\t</source>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>' + str(width) + '</width>\n')
        xml.write('\t\t<height>' + str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('</annotation>')
