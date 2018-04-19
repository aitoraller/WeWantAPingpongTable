import cv2
import numpy as np
from segmentation import *
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

cap = cv2.VideoCapture('N:\Temp\WeWantAPinpongTable\lateral\lateral_01.mp4')

cont_frames = 0
bbox_prev = []
bbox = []

while cap.isOpened():

    # Read frame
    ret, frame = cap.read()
    frame_r, scale = resize_image(frame, 640)

    # Localization mask
    mask_t = np.zeros(frame.shape[:2], np.uint8)
    if len(bbox) == 0:
        mask_t[100:980,0:1920] = 255
        # mask_t[100:980,1320:1920,] = 255
    elif len(bbox) == 4 and len(bbox_prev) == 0:
        x_min = max(bbox[0]-100, 0)
        y_min = max(bbox[1]-100, 0)
        mask_t[int(y_min):int(100+bbox[1]),int(x_min):int(100+bbox[0])] = 255
    else:
        est_loc = estimate_next_position(bbox_prev, bbox)
        x_min = max(est_loc[0] - 100, 0)
        y_min = max(est_loc[1] - 100, 0)
        mask_t[int(y_min):int(100 + est_loc[1]), int(x_min):int(100 + est_loc[0])] = 255

    mask_lr = cv2.resize(mask_t, (0, 0), fx=scale, fy=scale)

    # Ball segmentation
    #bbox_new = segment_ball_up(frame_r, mask_lr)
    bbox_new = segment_ball(frame_r, mask_lr)
    bbox_new = [x/scale for x in bbox_new]

    #bbox_new = []

    # BBOX updates
    bbox_prev = bbox
    bbox = bbox_new

    cv2.imshow('frame', frame_r)
    cv2.imshow('mask_lr', mask_lr)

    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cont_frames += 1

cap.release()
cv2.destroyAllWindows()
