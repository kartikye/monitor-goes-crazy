
from yeelight.transitions import *
from yeelight import Flow, Bulb

bulb = Bulb("10.226.239.115",effect="smooth", duration=100)

from PIL import ImageGrab
import time
import os
import colorsys

DECIMATE = 10
bulb.turn_on()
bulb.start_music()
bulb.effect = "sudden"
bulb.duration = 200

old_hsv = [1,1,1]

while True:
	a = time.time()
	red   = 1
	green = 1
	blue  = 1
	
	image = ImageGrab.grab()
	width = image.size[0]
	height = image.size[1]
	image = image.load()  # take a screenshot
	for y in range(0, height, DECIMATE):  #loop over the height
		for x in range(0, width, DECIMATE):  #loop over the width
			color = image[x, y]  #grab a pixel
			red = red + color[0]
			green = green + color[1]
			blue = blue + color[2]
	red = (( red / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
	green = ((green / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
	blue = ((blue / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
	try:
		#bulb.set_brightness((0.2126*red + 0.7152*green + 0.0722*blue)/ 255 * 100)
		#//bulb.set_rgb(int(red), int(green), int(blue))
		h = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
		goal = [int(h[0] * 360), int(h[1] * 100), int(h[2] * 100)]
		bulb.set_hsv(goal[0], goal[1], goal[2])
		'''while old_hsv[0] != goal[0] or old_hsv[1] != goal[1] or old_hsv[2] != goal[2]:
			if old_hsv[0] != goal[0]:
				if old_hsv[0] < goal[0]:
					old_hsv[0] +=1
				else:
					old_hsv[0] -=1

			if old_hsv[1] != goal[1]:
				if old_hsv[1] < goal[1]:
					old_hsv[1] +=1
				else:
					old_hsv[1] -=1

			if old_hsv[2] != goal[2]:
				if old_hsv[2] < goal[2]:
					old_hsv[2] +=1
				else:
					old_hsv[2] -=1
			print("B", time.time()-a)
			bulb.set_hsv(old_hsv[0], old_hsv[1], old_hsv[2])'''
		old_hsv = goal
		
	except Exception as e:
		print(e)

import atexit
atexit.register(lambda:bulb.stop_music())
