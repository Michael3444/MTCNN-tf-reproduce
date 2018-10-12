# -*- coding:utf-8 -*-

import numpy as np
import os

def IOU(bbox,bboxes):

    area = (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)
    areas = (bboxes[:,2] - bboxes[:,0] + 1) * (bboxes[:,3] - bboxes[:,1] + 1)

    x1 = np.maximum(bbox[0], bboxes[:, 0])
    y1 = np.maximum(bbox[1], bboxes[:, 1])
    x2 = np.minimum(bbox[2], bboxes[:, 2])
    y2 = np.minimum(bbox[3], bboxes[:, 3])

    w = np.maximum(0,x2-x1+1)
    h = np.maximum(0,y2-y1+1)

    intersection = w * h * 1.0
    iou = intersection / (area + areas - intersection)

    return iou

def ensure_dir_exists(path):

    if not os.path.exists(path):
        os.mkdir(path)

def convert_to_square(bbox):

    square_bbox = bbox.copy()

    h = bbox[:, 3] - bbox[:, 1]
    w = bbox[:, 2] - bbox[:, 0]
    max_side = np.maximum(h, w)
    square_bbox[:, 0] = bbox[:, 0] + w * 0.5 - max_side * 0.5
    square_bbox[:, 1] = bbox[:, 1] + h * 0.5 - max_side * 0.5
    square_bbox[:, 2] = square_bbox[:, 0] + max_side - 1
    square_bbox[:, 3] = square_bbox[:, 1] + max_side - 1

    return square_bbox