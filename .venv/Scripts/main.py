import cv2
import numpy as np
import csv
import tkinter as tk
from tkinter import filedialog



# Define HSV color range (example: red)
lower_color = np.array([0, 0, 230])
upper_color = np.array([10, 10, 255])

# Open video
def getvideo():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])



def Analyze():
    cap = cv2.VideoCapture(video_path)

    # Open CSV file for writing
    csv_file = open('particle_data.csv', mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Frame', 'Particle_ID', 'X', 'Y', 'Width', 'Height'])  # Header

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("Tracking", frame)


        print(f"Frame {frame_count}: {len(contours)} particles found")

        for i, cnt in enumerate(contours, start=1):
            x, y, w, h = cv2.boundingRect(cnt)
            csv_writer.writerow([frame_count, i, x, y, w, h])

    cap.release()
    csv_file.close()
    print("CSV export complete: 'particle_data.csv'")

def on_click(event):
    global lower_color, upper_color, picked_hsv
    # Get clicked coordinates
    x, y = event.x, event.y

    # Convert PIL coords to OpenCV
    clicked_bgr = first_frame[y, x]
    clicked_hsv = cv2.cvtColor(np.uint8([[clicked_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    picked_hsv = clicked_hsv

    # Set HSV range ±10 on hue, and generous ranges for S/V
    h, s, v = int(clicked_hsv[0]), int(clicked_hsv[1]), int(clicked_hsv[2])
    lower_color = np.array([max(h - 10, 0), max(s - 50, 0), max(v - 50, 0)])
    upper_color = np.array([min(h + 10, 179), min(s + 50, 255), min(v + 50, 255)])

    print(f"Picked HSV: {clicked_hsv}")
    print(f"Set color range:\n  Lower: {lower_color}\n  Upper: {upper_color}")
    root.destroy()  # Close window once selected


def getcolor():

    selected_color = None

    def pick_color(event, x, y, flags, param):
        global selected_color
        if event == cv2.EVENT_LBUTTONDOWN:
            selected_color = frame[y, x]
            print(f"Selected BGR color: {selected_color}")

            lower_color = np.clip(selected_color - 20, 0, 255)
            upper_color = np.clip(selected_color + 20, 0, 255)

            print(f"Lower bound: {lower_color}")
            print(f"Upper bound: {upper_color}")

            cv2.destroyAllWindows()

    path = video_path
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        exit()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Cannot read first frame.")
        exit()

    cv2.namedWindow("Select Color", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select Color", pick_color)

    cv2.imshow("Select Color", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
