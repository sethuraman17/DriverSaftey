from datetime import datetime
import cv2
import numpy as np
import csv

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 80)
fontScale = 3
color = (0, 0, 255)
thickness = 4
flag = False

# Initialize a set to store unique lane change events
unique_lane_change_events = set()

def driver_function():
    cap = cv2.VideoCapture("1.mov")
    while True:
        ret, frame = cap.read()
        frame = frame_processor(frame)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

    # Save unique lane change events to CSV file
    save_to_csv()

def frame_processor(frame):
    global flag

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    area = np.array(
        [
            (-100, 900),
            (1300, 900),
            (950, 600),
            (300, 600),
        ]
    )
    leftArea = np.array(
        [
            (-200, 900),
            (100, 900),
            (500, 600),
            (300, 600),
        ]
    )
    rightArea = np.array(
        [
            (1100, 900),
            (1400, 900),
            (950, 600),
            (800, 600),
        ]
    )
    maskArea = np.zeros_like(hsv)
    maskAreaLeft = np.zeros_like(hsv)
    maskAreaRight = np.zeros_like(hsv)

    cv2.fillPoly(maskArea, np.int32([area]), (255, 255, 255))
    cv2.fillPoly(maskAreaLeft, np.int32([leftArea]), (255, 255, 255))
    cv2.fillPoly(maskAreaRight, np.int32([rightArea]), (255, 255, 255))

    maskedImage = cv2.bitwise_and(hsv, maskArea)

    maskedImageLeft = cv2.bitwise_and(hsv, maskAreaLeft)
    maskedImageRight = cv2.bitwise_and(hsv, maskAreaRight)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_white = np.array([0, 0, 120])
    upper_white = np.array([255, 255, 255])

    mask_yellow = cv2.inRange(maskedImage, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(maskedImage, lower_white, upper_white)
    mask_white_left = cv2.inRange(maskedImageLeft, lower_white, upper_white)
    mask_white_right = cv2.inRange(maskedImageRight, lower_white, upper_white)
    mask = mask_white

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contoursLeft, _ = cv2.findContours(
        mask_white_left, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contoursRight, _ = cv2.findContours(
        mask_white_right, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    lane_lines = []
    lane_lines_left = []
    lane_lines_right = []

    for contour in contours:
        if cv2.contourArea(contour) < 6000 and cv2.contourArea(contour) > 1000:
            lane_lines.append(contour)

    for contour in contoursLeft:
        if cv2.contourArea(contour) < 6000 and cv2.contourArea(contour) > 1000:
            lane_lines_left.append(contour)

    for contour in contoursRight:
        if cv2.contourArea(contour) < 6000 and cv2.contourArea(contour) > 1000:
            lane_lines_right.append(contour)

    for lane_line in lane_lines_left:
        cv2.drawContours(frame, [lane_line], -1, (0, 0, 255), 2)
    for lane_line in lane_lines_right:
        cv2.drawContours(frame, [lane_line], -1, (0, 0, 255), 2)

    start = datetime.now()

    if len(contoursLeft) < 1 or len(contoursRight) < 1:
        print("---- Lane Change ----")

        frame = cv2.putText(
            frame, "Lane Change", org, font, fontScale, color, thickness, cv2.LINE_AA
        )

        # Check if the event is unique before storing it
        event_key = (start.strftime('%H:%M:%S'), 'Left to Right' if len(contoursRight) > 0 else 'Right to Left')
        if event_key not in unique_lane_change_events:
            unique_lane_change_events.add(event_key)

            # No need to append, as it is a set

        flag = True

    else:
        if flag:
            flag = False

    return frame

def save_to_csv():
    # Specify the CSV file path
    csv_file_path = 'lane_change_events.csv'

    # Write unique lane change events to CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        fieldnames = ['timestamp', 'direction']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for event in unique_lane_change_events:
            writer.writerow({'timestamp': event[0], 'direction': event[1]})


if __name__ == "__main__":
    driver_function()
