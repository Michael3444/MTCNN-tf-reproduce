# -*- coding:utf-8 -*-
import sys
sys.path.append('../12net')
import os,time,math,cv2
import numpy as np
import numpy.random as npr
from utils import IOU,ensure_dir_exists

anno_file = 'trainImageList.txt'
net = 'Pnet'

landmark_save_dir = '../12net/12/train_PNet_landmark_aug'
save_dir = '../12net/12'
ensure_dir_exists(save_dir)
ensure_dir_exists(landmark_save_dir)


def GenerateData(annos, save_dir, net, augment=False):

    if net == "PNet":
        size = 12
    elif net == "RNet":
        size = 24
    elif net == "ONet":
        size = 48
    else:
        raise Exception('Invalid net!')

    f = open(os.path.join(save_dir, 'landmark_%s_aug.txt' %size),'w')
    data = parsetxt(annos)

    for img_path, bbox, landmarkGT in data:

        img = cv2.imread(img_path)
        assert img is not None
        height, width, channle = img.shape









def parsetxt(anno_file):

    result = []
    with open(anno_file, 'r') as f:
        annos = f.readlines()
    for anno in annos:
        components = anno.strip().split(' ')
        img_path = components[0]
        bbox = map(int, components[1:5])
        landmark = np.asarray(map(float, components[5:])).reshape(5, 2)
        result.append((img_path, bbox, landmark))
    return result



if __name__ == '__main__':



