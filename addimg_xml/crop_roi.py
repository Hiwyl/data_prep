# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 09:25:17 2018
裁剪
@author: wyl
"""

import cv2
import os
import xml.etree.ElementTree as et
import voc_xml
import utils
from voc_xml import CreateXML

def crop_img_xml_from_dir(
        imgs_dir,
        xmls_dir,
        imgs_save_dir,
        xmls_save_dir,
        img_suffix,
        name_suffix,
        dsize,iou_thr):
    for root, dirs, files in os.walk(xmls_dir):
        print(root,dirs,files)
        for xml_name in files:
            xml_file = os.path.join(xmls_dir, xml_name)
            print('xml:', xml_file)
            #打开xml文档
            dom = et.parse(xml_file)
            root = dom.getroot()         
            for ele in root.findall("object"):
                for point in ele.findall("bndbox"):
                    xmin=point.find("xmin").text
                    ymax=point.find("ymax").text
            img_file = None
            for suffix in img_suffix:
                # print(os.path.join(imgs_dir,xml_name.split('.')[0]+suffix))
                if os.path.exists(
                    os.path.join(
                        imgs_dir,
                        xml_name.split('.')[0] +
                        suffix)):
                    img_file = os.path.join(
                        imgs_dir, xml_name.split('.')[0] + suffix)
                    break
            if img_file is None:
                print("there has no image for ", xml_name)
                continue
            print("img_file:", img_file)
            img = cv2.imread(img_file)
    
            imgh, imgw, n_channels = img.shape
            crop_imgw, crop_imgh = dsize
    
            crop_top_left_x, crop_top_left_y = int(xmin)-100 ,int(ymax)-100
            
            croped_img_name = xml_name.split('.')[0] + '_' + name_suffix +\
                        str(crop_top_left_x) + '_' + str(crop_top_left_y) +\
                        '_wh' + str(crop_imgw) + 'x' + str(crop_imgh) +\
                        '.' + img_file.split('.')[-1]
            croped = crop_img_xml(
                img,
                voc_xml.get_xml_tree(xml_file),
                croped_img_name,
                crop_top_left_x,
                crop_top_left_y,
                crop_imgw,
                crop_imgh,
                iou_thr)
            imgcrop, xmlcrop = croped[0], croped[1]
            cv2.imwrite(
                os.path.join(
                    imgs_save_dir,
                    croped_img_name),
                imgcrop)
            xmlcrop.save_xml(
                xmls_save_dir,
                croped_img_name.split('.')[0] +
                '.xml')

def crop_img(src, top_left_x, top_left_y, crop_w, crop_h):
    '''裁剪图像
    Args:
        src: 源图像
        top_left,top_right:裁剪图像左上角坐标
        crop_w,crop_h：裁剪图像宽高
    return：
        crop_img:裁剪后的图像
        None:裁剪尺寸错误
    '''
    rows, cols, n_channel = src.shape
    row_min, col_min = int(top_left_y), int(top_left_x)
    row_max, col_max = int(row_min + crop_h), int(col_min + crop_w)
    if row_max > rows:
        row_max=rows
    elif col_max > cols:
        col_max = cols
        # print("crop size err: src->%dx%d,crop->top_left(%d,%d) %dx%d" %
        #       (cols, rows, col_min, row_min, int(crop_w), int(crop_h)))
        # return None
    crop_img = src[row_min:row_max, col_min:col_max]
    return crop_img


def crop_xy(x, y, top_left_x, top_left_y, crop_w, crop_h):
    ''' 坐标平移变换
    Args:
        x,y:待变换坐标
        top_left_x,top_left_y:裁剪图像左上角坐标
        crop_w,crop_h:裁剪部分图像宽高
    return:
        crop_x,crop_y
    '''
    crop_x = int(x - top_left_x)
    crop_y = int(y - top_left_y)
    crop_x = utils.confine(crop_x, 0, crop_w - 1)
    crop_y = utils.confine(crop_y, 0, crop_h - 1)
    return crop_x, crop_y


def crop_box(box, top_left_x, top_left_y, crop_w, crop_h, iou_thr=0.5):
    '''目标框坐标平移变换
    Args:
        box:目标框坐标[xmin,ymin,xmax,ymax]
        top_left_x,top_left_y:裁剪图像左上角坐标
        crop_w,crop_h:裁剪部分图像宽高
        iou_thr: iou阈值,去除裁剪后过小目标
    return:
        crop_box:平移变换结果[xmin,ymin,xmax,ymax]
    '''
    xmin, ymin = crop_xy(box[0], box[1], top_left_x,
                         top_left_y, crop_w, crop_h)
    xmax, ymax = crop_xy(box[2], box[3], top_left_x,
                         top_left_y, crop_w, crop_h)
    croped_box = [xmin, ymin, xmax, ymax]
    if utils.calc_iou([0, 0, box[2] - box[0], box[3] - box[1]],
                      [0, 0, xmax - xmin, ymax - ymin]) < iou_thr:
        croped_box = [0, 0, 0, 0]
    return croped_box


def crop_xml(
        crop_img_name,
        xml_tree,
        top_left_x,
        top_left_y,
        crop_w,
        crop_h,
        iou_thr=0.5):
    '''xml目标框裁剪变换
    Args:
        crop_img_name:裁剪图片命名
        xml_tree：待crop的xml ET.parse()
        top_left_x,top_left_y: 裁剪图像左上角坐标
        crop_w,crop_h: 裁剪图像宽高
        iou_thr: iou阈值
    return:
        createdxml : 创建的xml CreateXML对象
    '''
    root = xml_tree.getroot()
    size = root.find('size')
    depth = int(size.find('depth').text)
    createdxml = CreateXML(crop_img_name, int(crop_w), int(crop_h), depth)
    for obj in root.iter('object'):
        obj_name = obj.find('name').text
        xml_box = obj.find('bndbox')
        xmin = int(xml_box.find('xmin').text)
        ymin = int(xml_box.find('ymin').text)
        xmax = int(xml_box.find('xmax').text)
        ymax = int(xml_box.find('ymax').text)
        box = crop_box([xmin, ymin, xmax, ymax], top_left_x,
                       top_left_y, crop_w, crop_h, iou_thr)
        if (box[0] >= box[2]) or (box[1] >= box[3]):
            continue
        createdxml.add_object_node(obj_name, box[0], box[1], box[2], box[3])
    return createdxml


def crop_img_xml(
        img,
        xml_tree,
        crop_img_name,
        top_left_x,
        top_left_y,
        crop_w,
        crop_h,
        iou_thr):
    '''裁剪图像和xml目标框
    Args:
        img：源图像
        crop_img_name:裁剪图片命名
        xml_tree：待crop的xml ET.parse()
        top_left_x,top_left_y: 裁剪图像左上角坐标
        crop_w,crop_h: 裁剪图像宽高
        iou_thr: iou阈值
    return:
        croped_img,croped_xml : 裁剪完成的图像和xml文件
        None:裁剪尺寸错误
    '''
    croped_img = crop_img(img, top_left_x, top_left_y, crop_w, crop_h)
    if croped_img is None:
        return None
    croped_xml = crop_xml(
        crop_img_name,
        xml_tree,
        top_left_x,
        top_left_y,
        crop_w,
        crop_h,
        iou_thr)
    return croped_img, croped_xml


if __name__=="__main__":
    imgs_dir = 'data/img/'
    xmls_dir = 'data/xml/'
    
    imgs_save_dir = 'data/crop_imgs/'
    if not os.path.exists(imgs_save_dir):
        os.makedirs(imgs_save_dir)
    xmls_save_dir = 'data/crop_xmls/'
    if not os.path.exists(xmls_save_dir):
        os.makedirs(xmls_save_dir)
    img_suffix = ['.jpg', '.png', '.bmp']
    name_suffix = 'crop'  # 命名标识
    dsize = (512,512)  # 指定裁剪尺度
    iou_thr=0.5
    
    crop_img_xml_from_dir(
        imgs_dir,
        xmls_dir,
        imgs_save_dir,
        xmls_save_dir,
        img_suffix,
        name_suffix,
        dsize,iou_thr)