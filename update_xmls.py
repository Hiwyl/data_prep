# -*- coding: utf-8 -*-
"""
@Author :       wyl
@Email :  wangyl306@163.com
"""
import os
import xml.etree.ElementTree as ET

current_path = os.path.abspath(__file__)

folder_path = os.path.split(current_path)


#图片路径
ann_dir="Annotations"
saved_path="rename_xml"
if not os.path.exists(saved_path):
    os.makedirs(saved_path)
anns=os.listdir(ann_dir)
for ann in anns:
    updateTree = ET.parse(os.path.join(ann_dir,ann))  # 读取待修改文件
    root = updateTree.getroot()
    sub = root.find("folder")
    sub.text =  "VOC2007"

    sub = root.find("filename")
    sub.text = ann.split(".")[0]+".jpeg"

    try:
        sub = root.find("path")
        sub.text =folder_path[0]+"/JPEGImages/"+ ann.split(".")[0] + ".jpeg"
    except:
        newEle = ET.Element("path")  # 创建新节点并添加为root的子节点
        # newEle.attrib = {"name": "NewElement", "age": "20"}
        newEle.text = folder_path[0]+"/JPEGImages/"+ ann.split(".")[0] + ".jpeg"
        root.append(newEle)


    updateTree.write(os.path.join(saved_path,ann))  # 写回原文件


