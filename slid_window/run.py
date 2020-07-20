# -*- coding: utf-8 -*-
"""
@Author :       wyl
@Email :  wangyl306@163.com
"""
import cv2
import os
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize[1]):
        for x in range(0, image.shape[1], stepSize[0]):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])



if __name__ == '__main__':
    imgs_path="./images"
    save_dir="./slid_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir) 
    for file in os.listdir(imgs_path):
        img=os.path.join(imgs_path,file)
        image = cv2.imread(img)
    
        (winW, winH) = (1024,1024) #切分尺寸
        stepSize = (1024,1024)  #滑动步长
        cnt = 0
        for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
            # since we do not have a classifier, we'll just draw the window
            clone = image.copy()
            cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 4)
            cv2.namedWindow('orign_images',0)
            cv2.imshow("orign_images", clone)
            cv2.waitKey(1000)
    
            slice = image[y:y+winH,x:x+winW]
            cv2.namedWindow('sliding_slice',0)
            cv2.imshow('sliding_slice', slice)
            cv2.waitKey(1000)
            cnt = cnt + 1
            #save
            # cv2.imwrite(save_dir+"/{0}_{1}.jpg".format(file.split(".")[0], cnt),slice)
    cv2.destroyAllWindows()



