import cv2
import numpy as np
import random

roi = None

upper_color = np.array([255, 255, 255], dtype='uint8')
lower_color = np.array([0, 100, 100], dtype='uint8')


COLORS = ['R', 'G', "B", 'Y']

red_mask = [np.array([0, 100, 50]), np.array([6, 255, 255])]
green_mask = [np.array([30, 100, 50]), np.array([70, 255, 255])]
blue_mask = [np.array([80, 100, 50]), np.array([110, 255, 255])]
yellow_mask = [np.array([20, 100, 50]), np.array([25, 255, 255])]


def set_upper(x):
    global upper_color
    upper_color[0] = x


def set_lower(x):
    global lower_color
    lower_color[0] = x


cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)


def find_circle(frame_inp, color):
    blurred = cv2.GaussianBlur(frame_inp, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, color[0], color[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 30:
            return int(curr_x), int(curr_y), int(radius)
    return None


if __name__ == '__main__':
    while cam.isOpened():
        ret, frame = cam.read()

        red_ball = find_circle(frame, red_mask)
        green_ball = find_circle(frame, green_mask)
        blue_ball = find_circle(frame, blue_mask)
        yellow_ball = find_circle(frame, yellow_mask)

        if red_ball:
            cv2.circle(frame, (red_ball[0], red_ball[1]), red_ball[2], (0, 255, 255), 2)
        if green_ball:
            cv2.circle(frame, (green_ball[0], green_ball[1]), green_ball[2], (0, 255, 255), 2)
        if blue_ball:
            cv2.circle(frame, (blue_ball[0], blue_ball[1]), blue_ball[2], (0, 255, 255), 2)
        if yellow_ball:
            cv2.circle(frame, (yellow_ball[0], yellow_ball[1]), yellow_ball[2], (0, 255, 255), 2)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        cv2.imshow("Camera", frame)

    cam.release()
    cv2.destroyAllWindows()
