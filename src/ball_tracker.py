
import cv2
import sys
import numpy as np

video_file = "N:/Temp/WeWantAPinpongTable/up/up_01.mp4"
image_test = "N:/Temp/WeWantAPinpongTable/up/up_01_frames/scene00015.png"
red_folder = "N:/Temp/WeWantAPinpongTable/up/up_01_red_tracker"

table_tl = (266,240)
table_tm = (929,243)
table_tr = (1522,245)
table_br = (1544,876)
table_bm = (938,883)
table_bl = (249,891)

first_position = (549,588,47,44)

def calculate_direction(bbox_prev, bbox):
    c_prev_x = (bbox_prev[0] + bbox_prev[2]) / 2
    c_prev_y = (bbox_prev[1] + bbox_prev[3]) / 2
    c_x = (bbox[0] + bbox[2]) / 2
    c_y = (bbox[1] + bbox[3]) / 2
    return c_x-c_prev_x, c_y-c_prev_y

def calculate_speed(bbox_prev, bbox, fps=30):
    #desp/(1/fps)
    sec = 1/fps
    c_prev_x = (bbox_prev[0]+bbox_prev[2])/2
    c_prev_y = (bbox_prev[1] + bbox_prev[3]) / 2
    c_x = (bbox[0] + bbox[2]) / 2
    c_y = (bbox[1] + bbox[3]) / 2
    desp = np.squrt((c_x-c_prev_x)^2+(c_y-c_prev_y)^2)
    return fps/sec

def estimate_next_position(bbox_prev, bbox):
    dx, dy = calculate_direction(bbox_prev, bbox)
    next_pos = [bbox[0]+dx,bbox[1]+dy,bbox[2],bbox[3]]
    return next_pos


if __name__ == "__main__":

    tracker = cv2.TrackerMIL_create()

    # Read video
    video = cv2.VideoCapture(video_file)

    # Exit if video not opened.
    if not video.isOpened():
        print "Could not open video"
        sys.exit()

    for i in range(50):
        ret, frame = video.read()

    bbox = cv2.selectROI("tracking", frame[:,:,2])
    ok = tracker.init(frame, bbox)

    while video.isOpened():
        ret, frame = video.read()
        #red_channel = frame[:,:,2]
        ok, bbox = tracker.update(frame[:,:,2])
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        #cv2.rectangle(frame,(first_position[0],first_position[1]),(first_position[0]+first_position[2],first_position[1]+first_position[3]),(0,0,255),3)
        cv2.imshow("Detection",frame)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
