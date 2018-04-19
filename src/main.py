import cv2
import numpy as np
from segmentation import segment_ball
from ball_tracker import *
from utils import resize_image

table_tl = (266,240)
table_tm = (929,243)
table_tr = (1522,245)
table_br = (1544,876)
table_bm = (938,883)
table_bl = (249,891)

table_ls = (67,968)
table_ms = (993,954)
table_rs = (1849,941)

cap = cv2.VideoCapture('C:/Users/user/Documents/Workspace/Python/WeWantAPingpongTable/data/lateral/lateral_01.mp4')


cont_frames = 0
while cap.isOpened():
    ret, frame = cap.read()

    frame_r, scale = resize_image(frame_r, 640)

    if cont_frames == 0:
        mask_l = np.zeros(frame.shape[:2])
        mask_l[0:200,500:968] = 1
        mask_l[1720:1920, 500:968] = 1
        mask_lr = cv2.rescale(mask_l, (0,0), fx=scale, fy=scale)
    else
        estimate_next_position(bbox_prev, bbox)

    segment_ball(frame_r)
    cv2.imshow('frame', frame_r)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cont_frames += 1

cap.release()
cv2.destroyAllWindows()
