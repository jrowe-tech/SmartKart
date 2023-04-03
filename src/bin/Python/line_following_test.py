import numpy as np
import cv2

cam = cv2.VideoCapture(0)
_, img = cam.read()

# Set test variables
crop_left = None
crop_right = None
crop_bottom=None
crop_top=100
max_speed = 80
cam_height, cam_width, _ = img.shape

#Grab IMAGE and Crop Bottom
img = img[crop_left: crop_right, crop_bottom:crop_top]

if crop_left and crop_right:
    centerX = (crop_right - crop_left) // 2
else:
    centerX = cam_width // 2

if crop_right:
    max_error = crop_right - centerX
else:
    max_error = cam_width // 2

# Create HSV Mask
hsv_low = (0, 0, 0)
hsv_high = (360, 180, 180)
mask = cv2.inRange(img, hsv_low, hsv_high)

# Grab Pixel Coordinates of Every White Pixel
pixels = np.argwhere(img == 1) # OR 1!

num_pixels = len(pixels)

# Grab Average Of Mask Pixels
avgX = 0
# avgY = 0
for pixel in pixels:
    avgX += pixel[0]
    # avgY += pixel[1]

avgX /= num_pixels
# avgY /= num_pixels

# Scale distance from center to avgPixel Location
error = (avgX - centerX) / max_error

# Change velocity proportionally!
v = error * max_speed

def set_pwm():
    pwm = 20
    if v > 0:
        pwm.setPWM(2, v) # [FOR STEERING]
        pwm.clearPWM(3)
    elif v < 0:
        pwm.setPWM(3, v) # [FOR STEERING]
        pwm.clearPWM(2)
    else:
        pwm.clearPWM(2)
        pwm.clearPWM(3)
