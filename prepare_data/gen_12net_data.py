# -*- coding:utf-8 -*-

import sys
sys.path.append('../12net')
import numpy as np
import os,cv2
import numpy.random as npr
from utils import IOU,ensure_dir_exists

anno_file = 'wider_face_train.txt'
img_dir = 'WIDER_train/images'

pos_save_dir = '../12net/12/positive'
part_save_dir = '../12net/12/part'
neg_save_dir = '../12net/12/negative'
save_dir = '../12net/12'

ensure_dir_exists(save_dir)
ensure_dir_exists(pos_save_dir)
ensure_dir_exists(part_save_dir)
ensure_dir_exists(neg_save_dir)

f1 = open(os.path.join(save_dir, 'pos_12.txt'), 'w')
f2 = open(os.path.join(save_dir, 'neg_12.txt'), 'w')
f3 = open(os.path.join(save_dir, 'part_12.txt'), 'w')

with open(anno_file, 'r') as f:
    annotations = f.readlines()

num = len(annotations)
print '%d pics in total' %num

p_idx = 0
d_idx = 0
n_idx = 0
idx = 0
box_idx = 0

for annotation in annotations:
    # for each pics
    annotation = annotation.strip().split(' ')
    img_path = annotation[0]
    bbox = map(float, annotation[1:])
    bboxes = np.array(bbox, dtype=np.float32).reshape(-1, 4)
    img = cv2.imread(os.path.join(img_dir, img_path + '.jpg'))
    idx += 1
    if idx % 100 == 0:
        print idx, 'images done!'

    height, width, channel = img.shape

    neg_num = 0
    while neg_num < 50:
        size = npr.randint(12, min(width, height) / 2)  # 12 or 40
        nx = npr.randint(0, width - size)
        ny = npr.randint(0, height - size)
        crop_box = np.array([nx, ny, nx + size, ny + size])

        iou = IOU(crop_box, bboxes)

        cropped_img = img[ny:ny+size, nx:nx+size,:]
        resized_img = cv2.resize(cropped_img, (12, 12), interpolation=cv2.INTER_LINEAR)

        if np.max(iou) < 0.3:
             save_file = os.path.join(neg_save_dir, '%s.jpg' %n_idx)
             f2.write('12/negative/%s' % n_idx + ' 0\n')
             cv2.imwrite(save_file, resized_img)
             n_idx += 1
             neg_num += 1
    for box in bboxes:
        # for each ground truth bbox
        x1, y1, x2, y2 = box
        w = x2 - x1 + 1
        h = y2 - y2 + 1
        # ignore small faces
        if max(w, h) < 40 or x1 < 0 or y1 < 0:
            continue
        for i in range(5):
            size = npr.randint(12, min(width, height) / 2)
            # delta_x and delta_y are offsets of (x1, y1)
            delta_x = npr.randint(max(-size, -x1), w)
            delta_y = npr.randint(max(-size, -y1), h)
            nx1 = int(max(0, x1 + delta_x))
            ny1 = int(max(0, y1 + delta_y))
            if nx1 + size > width or ny1 + size > height:
                continue
            crop_box = np.array([nx1, ny1, nx1 + size, ny1 + size])
            iou = IOU(crop_box, bboxes)

            cropped_img = img[ny1: ny1 + size, nx1: nx1 + size, :]
            resized_img = cv2.resize(cropped_img, (12, 12), interpolation=cv2.INTER_LINEAR)

            if np.max(Iou) < 0.3:
                # Iou with all gts must below 0.3
                save_file = os.path.join(neg_save_dir, "%s.jpg" % n_idx)
                f2.write('12/negative/%s' % n_idx + ' 0\n')
                cv2.imwrite(save_file, resized_img)
                n_idx += 1

        for i in range(20):
            size = npr.randint(int(min(w, h) * 0.8), np.ceil(1.25 * max(w, h)))

            # delta here is the offset of the bbox center
            delta_x = npr.randint(-0.2 * w, 0.2 * w)
            delta_y = npr.randint(-0.2 * h, 0.2 * h)

            nx1 = max(0, x1 + w / 2 + delta_x - size)
            ny1 = max(0, y1 + h / 2 + delta_y - size)
            nx2 = nx1 + size
            ny2 = nx2 + size

            if nx2 > width or ny2 > height:
                continue

            crop_box = np.array([nx1, ny1, nx2, ny2])

            offset_x1 = (x1 - nx1) / float(size)
            offset_y1 = (y1 - ny1) / float(size)
            offset_x2 = (x2 - nx2) / float(size)
            offset_y2 = (y2 - ny2) / float(size)

            cropped_img = img[int(ny1):int(ny2), int(nx1):int(nx2),:]
            reiszed_img = cv2.resize(cropped_img, (12, 12), interpolation=cv2.INTER_LINEAR)

            box_ = box.reshape(1,-1)
            if IOU(crop_box, box_) >= 0.65:
                save_file = os.path.join(pos_save_dir, '%s.jpg' %p_idx)
                f1.write('12/positive/%s' %p_idx + ' 1 %.2f %.2f %.2f %.2f\n' %(offset_x1, offset_y1, offset_x2, offset_y2))
                cv2.imwrite(save_file, resized_img)
                p_idx += 1

            elif IOU(crop_box, box_) >= 0.4:
                save_file = os.path.join(part_save_dir, '%s.jpg' % d_idx)
                f3.write('12/part/%s' % d_idx + ' -1 %.2f %.2f %.2f %.2f\n' % (offset_x1, offset_y1, offset_x2, offset_y2))
                cv2.imwrite(save_file, resized_img)
                d_idx += 1

    box_idx += 1
    print "%s images done, pos: %s part: %s neg: %s"%(idx, p_idx, d_idx, n_idx)
f1.close()
f2.close()
f3.close()
































