import cv2
import numpy as np

ballBGRLower = (5, 60, 140)
ballBGRUpper = (110, 125, 205)

ballBGRLowerUp = (25, 80, 170)
ballBGRUpperUp = (130, 180, 235)

ballBGRLowerUpHSV = (5, 80, 0)
ballBGRUpperUpHSV = (45, 255, 255)


def segment_ball(image, mask_aux=[]):

    image_ = image.copy()

    mask = cv2.inRange(image_, ballBGRLower, ballBGRUpper)
    mask = cv2.erode(mask, (5, 5), iterations=2)
    mask = cv2.dilate(mask, (5, 5), iterations=2)

    mask_playzone = np.zeros(mask.shape, dtype=np.uint8)
    mask_playzone[100:-30, 10:-10] = 255

    mask = cv2.bitwise_and(mask, mask_playzone)
    if mask_aux:
        mask = cv2.bitwise_and(mask, mask_aux)

    # cv2.imshow("mask", mask)
    # cv2.imshow("mask_playzone", mask_playzone)
    cv2.imshow("mask", mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only proceed if at least one contour was found
    bb = []
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        max_area = 0
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            ar = float(w) / h
            if 15 < area < 150 and 1/2 < ar < 2:
                cv2.rectangle(image_, (x, y), (x + w, y + h), (0, 255, 255), 2)
                if area > max_area:
                    max_area = area
                    x, y, w, h = cv2.boundingRect(cnt)
                    bb = [x, y, w, h]
    cv2.imshow("circle", image_)
    return bb


def segment_ball_up(image, mask_aux=[]):

    image_ = image.copy()

    mask = cv2.inRange(image_, ballBGRLowerUp, ballBGRUpperUp)
    mask = cv2.erode(mask, (5, 5), iterations=2)
    mask = cv2.dilate(mask, (5, 5), iterations=2)

    mask_playzone = np.zeros(mask.shape, dtype=np.uint8)
    mask_playzone[30:-30, 10:-10] = 255

    mask = cv2.bitwise_and(mask, mask_playzone)
    if mask_aux:
        mask = cv2.bitwise_and(mask, mask_aux)

    cv2.imshow("mask", mask )

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only proceed if at least one contour was found
    bb = []
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        max_area = 0
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            ar = float(w) / h
            if 15 < area < 400 and 1/3.5 < ar < 3.5:
                cv2.rectangle(image_, (x, y), (x + w, y + h), (0, 255, 255), 2)
                if area > max_area:
                    max_area = area
                    x, y, w, h = cv2.boundingRect(cnt)
                    bb = [x, y, w, h]

    cv2.imshow("circle", image_)
    return bb


def segment_ball_up_hsv(image):

    image_ = image.copy()

    mask = cv2.inRange(image_, ballBGRLowerUpHSV, ballBGRUpperUpHSV)
    mask = cv2.erode(mask, (5, 5), iterations=2)
    mask = cv2.dilate(mask, (5, 5), iterations=2)

    mask_playzone = np.zeros(mask.shape, dtype=np.uint8)
    mask_playzone[30:-30, 10:-10] = 255

    mask = cv2.bitwise_and(mask, mask_playzone)

    cv2.imshow("maskHSV", mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only proceed if at least one contour was found
    contours = []
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        print " "
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            ar = float(w) / h
            if area > 10:
                print area, ar
            if 15 < area < 400 and 1/3.5 < ar < 3.5:
                cv2.rectangle(image_, (x, y), (x + w, y + h), (0, 255, 255), 2)
                contours.append(cnt)
        cv2.imshow("circle_hsv", image_)
        return contours
