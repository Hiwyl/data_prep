# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import os

dot=[]
nick=[]
scratch=[]
DirName="data/VOCdevkit/VOC2007/Annotations"

filelist = os.listdir(DirName)

#打开xml文档
for file in filelist:
    dom = et.parse(DirName+"/"+file)
    root = dom.getroot() 
    # 查找根目录下面的子元素  
    for ele in root.findall("object"):
        name=ele.find("name").text
        
        if name=="dot":
            dot.append(file)
        elif name=="nick":
            nick.append(file)
        elif name == "scratch":
            scratch.append(file)
print("dot:",len(dot))
print("nick:",len(nick))
print("scratch:",len(scratch))

 
