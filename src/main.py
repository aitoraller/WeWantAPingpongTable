import cv2
import numpy as np
from segmentation import segment_ball
from utils import resize_image

cap = cv2.VideoCapture('C:/Users/user/Documents/Workspace/Python/WeWantAPingpongTable/data/lateral/lateral_01.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    frame, scale = resize_image(frame, 640)

    segment_ball(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
