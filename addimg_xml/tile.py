# -*- coding: utf-8 -*-
"""
@author:      wyl
@email: wangyl306@163.com
@data: Tue Jun 30 19:04:43 2020
"""
#使用移动滑窗进行tile
import cv2
import os
import voc_xml
import utils
from voc_xml import CreateXML


def tile_img(src, top_left_x, top_left_y, tile_w, tile_h):
    '''裁剪图像
    Args:
        src: 源图像
        top_left,top_right:裁剪图像左上角坐标
        tile_w,tile_h：裁剪图像宽高
    return：
        tile_img:裁剪后的图像
        None:裁剪尺寸错误
    '''
    rows, cols, n_channel = src.shape
    row_min, col_min = int(top_left_y), int(top_left_x)
    row_max, col_max = int(row_min + tile_h), int(col_min + tile_w)
    if row_max > rows or col_max > cols:
        print("tile size err: src->%dx%d,tile->top_left(%d,%d) %dx%d" %
              (cols, rows, col_min, row_min, int(tile_w), int(tile_h)))
        return None
    tile_img = src[row_min:row_max, col_min:col_max]
    return tile_img


def tile_xy(x, y, top_left_x, top_left_y, tile_w, tile_h):
    ''' 坐标平移变换
    Args:
        x,y:待变换坐标
        top_left_x,top_left_y:裁剪图像左上角坐标
        tile_w,tile_h:裁剪部分图像宽高
    return:
        tile_x,tile_y
    '''
    tile_x = int(x - top_left_x)
    tile_y = int(y - top_left_y)
    tile_x = utils.confine(tile_x, 0, tile_w - 1)
    tile_y = utils.confine(tile_y, 0, tile_h - 1)
    return tile_x, tile_y


def tile_box(box, top_left_x, top_left_y, tile_w, tile_h, iou_thr=0.5):
    '''目标框坐标平移变换
    Args:
        box:目标框坐标[xmin,ymin,xmax,ymax]
        top_left_x,top_left_y:裁剪图像左上角坐标
        tile_w,tile_h:裁剪部分图像宽高
        iou_thr: iou阈值,去除裁剪后过小目标
    return:
        tile_box:平移变换结果[xmin,ymin,xmax,ymax]
    '''
    xmin, ymin = tile_xy(box[0], box[1], top_left_x,
                         top_left_y, tile_w, tile_h)
    xmax, ymax = tile_xy(box[2], box[3], top_left_x,
                         top_left_y, tile_w, tile_h)
    tileed_box = [xmin, ymin, xmax, ymax]
    if utils.calc_iou([0, 0, box[2] - box[0], box[3] - box[1]],
                      [0, 0, xmax - xmin, ymax - ymin]) < iou_thr:
        tileed_box = [0, 0, 0, 0]
    return tileed_box


def tile_xml(
        tile_img_name,
        xml_tree,
        top_left_x,
        top_left_y,
        tile_w,
        tile_h,
        iou_thr=0.5):
    '''xml目标框裁剪变换
    Args:
        tile_img_name:裁剪图片命名
        xml_tree：待tile的xml ET.parse()
        top_left_x,top_left_y: 裁剪图像左上角坐标
        tile_w,tile_h: 裁剪图像宽高
        iou_thr: iou阈值
    return:
        createdxml : 创建的xml CreateXML对象
    '''
    root = xml_tree.getroot()
    size = root.find('size')
    depth = int(size.find('depth').text)
    createdxml = CreateXML(tile_img_name, int(tile_w), int(tile_h), depth)
    for obj in root.iter('object'):
        obj_name = obj.find('name').text
        xml_box = obj.find('bndbox')
        xmin = int(xml_box.find('xmin').text)
        ymin = int(xml_box.find('ymin').text)
        xmax = int(xml_box.find('xmax').text)
        ymax = int(xml_box.find('ymax').text)
        box = tile_box([xmin, ymin, xmax, ymax], top_left_x,
                       top_left_y, tile_w, tile_h, iou_thr)
        if (box[0] >= box[2]) or (box[1] >= box[3]):
            continue
        createdxml.add_object_node(obj_name, box[0], box[1], box[2], box[3])
    return createdxml


def tile_img_xml(
        img,
        xml_tree,
        tile_img_name,
        top_left_x,
        top_left_y,
        tile_w,
        tile_h,
        iou_thr):
    '''裁剪图像和xml目标框
    Args:
        img：源图像
        tile_img_name:裁剪图片命名
        xml_tree：待tile的xml ET.parse()
        top_left_x,top_left_y: 裁剪图像左上角坐标
        tile_w,tile_h: 裁剪图像宽高
        iou_thr: iou阈值
    return:
        tileed_img,tileed_xml : 裁剪完成的图像和xml文件
        None:裁剪尺寸错误
    '''
    tileed_img = tile_img(img, top_left_x, top_left_y, tile_w, tile_h)
    if tileed_img is None:
        return None
    tileed_xml = tile_xml(
        tile_img_name,
        xml_tree,
        top_left_x,
        top_left_y,
        tile_w,
        tile_h,
        iou_thr)
    return tileed_img, tileed_xml


def sliding_window(image,stepSize,windowsSize):
    for y in range(0,image.shape[0],stepSize[1]):
        for x in range(0,image.shape[1],stepSize[0]):
            yield (x,y,image[y:y+windowsSize[1],x:x+windowsSize[0]])

def tile_img_xml_from_dir(
        imgs_dir,
        xmls_dir,
        imgs_save_dir,
        xmls_save_dir,
        img_suffix,
        name_suffix,
        # tile_type='RANDOM_tile',
        # tile_n=1,
        dsize=(1024,1024),
        stepSize=(1024,1024),
        iou_thr=0.5):
    '''使用移动滑窗裁剪原始图片
    Args:
        imgs_dir,xmls_dir: 图片、原始xml文件存储路径
        imgs_save_dir，xmls_save_dir: 处理完成的图片、xml文件存储路径
        img_suffix: 图片可能的后缀名['.jpg','.png','.bmp',..]
        name_suffix: 处理完成的图片、xml的命名标识
        dsize:指定tile宽高（w,h）
        iou_thr: iou阈值
    '''
    winW,winH=dsize[0],dsize[1]
    for root, dirs, files in os.walk(xmls_dir):
        for xml_name in files:
            xml_file = os.path.join(xmls_dir, xml_name)
            print('xml:', xml_file)
            img_file = None
            for suffix in img_suffix:
                # print(os.path.join(imgs_dir,xml_name.split('.')[0]+suffix))
                if os.path.exists(
                    os.path.join(
                        imgs_dir,
                        xml_name.split('.')[0] + suffix)):
                    img_file = os.path.join(
                        imgs_dir, xml_name.split('.')[0] + suffix)
                    break
            if img_file is None:
                print("there has no image for ", xml_name)
                continue
            print("img_file:", img_file)
            img = cv2.imread(img_file)
            # print(img)
            imgh, imgw, n_channels = img.shape
            
            #移动滑窗裁剪
            for (tile_top_left_x,tile_top_left_y,window) in sliding_window(img,stepSize=stepSize,windowsSize=(winW,winH)):
                if window.shape[0] != winH or window.shape[1] !=winW:
                    continue
                # slice=img[y:y+winH,x:x+winW]

                tileed_img_name = xml_name.split('.')[0] + '_' + name_suffix +\
                    str(tile_top_left_x) + '_' + str(tile_top_left_y) +\
                    '_wh' + str(winW) + 'x' + str(winH) +\
                    '.' + img_file.split('.')[-1]
                tileed = tile_img_xml(
                    img,
                    voc_xml.get_xml_tree(xml_file),
                    tileed_img_name,
                    tile_top_left_x,
                    tile_top_left_y,
                    winW,
                    winH,
                    iou_thr)
                imgtile, xmltile = tileed[0], tileed[1]
                cv2.imwrite(
                    os.path.join(
                        imgs_save_dir,
                        tileed_img_name),
                    imgtile)
                xmltile.save_xml(
                    xmls_save_dir,
                    tileed_img_name.split('.')[0] +
                    '.xml')


def main():
    imgs_dir = 'data/img/'
    xmls_dir = 'data/xml/'
    imgs_save_dir = 'data/tile_imgs/'
    if not os.path.exists(imgs_save_dir):
        os.makedirs(imgs_save_dir)
    xmls_save_dir = 'data/tile_xmls/'
    if not os.path.exists(xmls_save_dir):
        os.makedirs(xmls_save_dir)
    img_suffix = ['.jpg', '.png', '.bmp']
    name_suffix = 'tile'  # 命名标识
    # tile_type = 'RANDOM_tile'  # ['RANDOM_tile','CENTER_tile','FIVE_tile']
    # tile_n = 15 # 每张原图 tile 5张图
    # 指定tile的尺寸
    dsize=(512,512)  #裁剪块的大小
    stepSize=(512,512) #宽高的移动步幅
    iou_thr = 0.2  # 裁剪后目标框大小与原框大小的iou值大于该阈值则保留
    tile_img_xml_from_dir(
        imgs_dir,
        xmls_dir,
        imgs_save_dir,
        xmls_save_dir,
        img_suffix,
        name_suffix,
        dsize,stepSize,
        iou_thr)
    


if __name__ == '__main__':
    main()
