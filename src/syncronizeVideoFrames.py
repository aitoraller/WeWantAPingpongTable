import cv2
import numpy as np
import json



def resize_image(image, max_size=640):
    image_resized = image.copy()
    height, width = image.shape[0:2]
    scale = 1
    if height > max_size or width > max_size:
        scale = float(max_size) / max([height, width])
        image_resized = cv2.resize(image, None, fx=scale, fy=scale)

    return image_resized, scale



numberVideo = '01'

names = ['N:/Temp/WeWantAPinpongTable/lateral/lateral_' + numberVideo + '.mp4', 'N:/Temp/WeWantAPinpongTable/up/up_' + numberVideo + '.mp4']
delay = json.load(open('N:/Temp/WeWantAPinpongTable/' + numberVideo + '.json'))



cap = [cv2.VideoCapture(names[0]), cv2.VideoCapture(names[1])]

cap[0].set(cv2.CAP_PROP_POS_FRAMES, delay['delayLateral'])
cap[1].set(cv2.CAP_PROP_POS_FRAMES, delay['delayUp'])


frames = [None] * len(names)
gray = [None] * len(names)
ret = [None] * len(names)

while True:

    for i,c in enumerate(cap):
        if c is not None:
            ret[i], frames[i] = c.read()


    image_Concat = []
    for i,f in enumerate(frames):
        if ret[i] is True:
            if (i==0):
                image_Concat = frames[i]
            if (i==1):
                image_Concat = np.concatenate((image_Concat, frames[i]), axis=1)
                [image_Concat, scaleImg] = resize_image(image_Concat, 1500)
                cv2.imshow('video', image_Concat)

    if cv2.waitKey(0) & 0xFF == ord('q'):
       break


for c in cap:
    if c is not None:
        c.release()

cv2.destroyAllWindows()

