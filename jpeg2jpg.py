import cv2
import glob

for file in glob.glob('/Users/wuyanqing/目标检测/数据/zhijian_car/train' + '/*.*'):
    if file.endswith('jpeg'):
        img = cv2.imread(file)
        cv2.imwrite(file.replace('jpeg', 'jpg'), img)
