#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------


import cv2
import pyautogui
import numpy as np

# Set the screen recording parameters
SCREEN_SIZE = (1920, 1080)  # Adjust this according to your screen resolution
OUTPUT_FILE = 'screen_record.mp4'  # Output file name

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, 20.0, SCREEN_SIZE)

try:
    while True:
        # Capture the screen and convert the image to BGR format
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Write the frame to the output file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Screen Recorder', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
finally:
    # Release the VideoWriter and destroy the OpenCV windows
    out.release()
    cv2.destroyAllWindows()
