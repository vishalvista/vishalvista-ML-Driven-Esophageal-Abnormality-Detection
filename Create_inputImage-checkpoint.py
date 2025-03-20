import cv2
import os
import sys
import time

# Reading input and setting the frames
inp = cv2.VideoCapture("C:\\Users\\Vishal R\\Downloads\\DownwardDog.mp4")

# Check if the video file opened successfully
if not inp.isOpened():
    print("Error: Unable to open video file.")
    sys.exit()

# Get total frame count to ensure we're processing all frames
total_frames = int(inp.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total frames in video: {total_frames}")

# Setting the starting frame (you can change this if needed)
inp.set(1, 400)

# Check if the directory for images exists, if not, create it
try:
    if not os.path.exists('inp_images'):
        os.makedirs('inp_images')
except OSError:
    print('Error creating input directory')

# Current frame number
curr_frame = 0

# Reads the frame and stores it in the directory
while True:
    inp.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)  # Set the current frame manually
    ret, frame = inp.read()

    # Check if frame is read successfully
    if not ret:
        print(f"Failed to read frame {curr_frame} or end of video.")
        break
    
    # Save the frame as an image
    name = './inp_images/inp_image_' + str(curr_frame) + '.jpg'
    print(f"Creating... {name}")
    cv2.imwrite(name, frame)
    
    # Increment the frame counter
    curr_frame += 1
    
    # Optional: add a small delay to help with frame processing
    time.sleep(0.1)

    # Stop if we've processed all frames
    if curr_frame >= total_frames:
        break

# Release the video capture object and close any OpenCV windows
inp.release()
cv2.destroyAllWindows()