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


def generate_square():
    data = [[1, 2], [3, 4]]
    col = COLORS.copy()
    for i in range(4):
        rand_int = random.randint(0, len(col)-1)
        if i < 2:
            data[0][i] = col[rand_int]
        else:
            data[1][i-2] = col[rand_int]
        del col[rand_int]
    return data



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


def find_line(red_ball, green_ball, blue_ball):
    if red_ball and green_ball and blue_ball:
        ball_data = [{"data": red_ball, "color": "R"},
                     {"data": green_ball, "color": "G"},
                     {"data": blue_ball, "color": "B"},
                     {"data": yellow_ball, "color": "Y"}]
        ball_data.sort(key=lambda x: x['data'][0])
        if ball_data[0]['color'] == colors[0] and ball_data[1]['color'] == colors[1] and ball_data[2]['color'] == colors[2] and ball_data[3]['color'] == colors[3]:
            cv2.putText(frame, f'WIN!!!', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (205, 92, 92))


def find_square(red_ball, green_ball, blue_ball, yellow_ball):
    if red_ball and green_ball and blue_ball and yellow_ball:
        ball_data = [{"data": red_ball, "color": "R"},
                     {"data": green_ball, "color": "G"},
                     {"data": blue_ball, "color": "B"},
                     {"data": yellow_ball, "color": "Y"}]
        ball_data.sort(key=lambda x: x['data'][1])
        ball_data = [[ball_data[0], ball_data[1]], [ball_data[2], ball_data[3]]]
        ball_data[0].sort(key=lambda x: x['data'][0])
        ball_data[1].sort(key=lambda x: x['data'][0])

        if ball_data[0][0]['color'] == square_colors[0][0] and ball_data[0][1]['color'] == square_colors[0][1]:
            if ball_data[1][0]['color'] == square_colors[1][0] and ball_data[1][1]['color'] == square_colors[1][1]:
                cv2.putText(frame, f'WIN!!!', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (205, 92, 92))


if __name__ == '__main__':
    colors = COLORS
    random.shuffle(colors)
    square_colors = generate_square()
    print(square_colors)
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

        # find_line(red_ball, green_ball, blue_ball)
        find_square(red_ball, green_ball, blue_ball, yellow_ball)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        cv2.imshow("Camera", frame)

    cam.release()
    cv2.destroyAllWindows()
