import os

sonDirName="/root/projects/ihi_mmdetection/data/standard_test"

filelist = os.listdir(sonDirName)
total_num = len(filelist)
i = 1
for item in filelist:
    # print(item)
    if item.endswith('.jpeg') or item.endswith('.bmp'):
        src = os.path.join(os.path.abspath(sonDirName), item)
        dst = os.path.join(os.path.abspath(sonDirName), item.split(".")[0]+'.jpg')
        # print(dst)
        try:
            os.rename(src, dst)
            print('converting %s to %s ...' % (src, dst))
            i = i + 1
        except:
            continue

print('total %d to rename & converted %d jpgs' % (total_num, i - 1))