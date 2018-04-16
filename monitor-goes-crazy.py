from yeelight.transitions import *
from yeelight import Flow, Bulb

bulb_ip_address = "10.225.243.35" #set ip adress here

bulb = Bulb(bulb_ip_address, effect="smooth", duration=100)

from PIL import ImageGrab
import time
import os
import colorsys

DECIMATE = 10 #increase this to reduce the computational requirments

try:
	bulb.turn_on()
except:
	print('Unable to connect to bulb. Please check the IP address.')
	exit()
	
bulb.start_music()
bulb.effect = "sudden"
bulb.duration = 200

old_hsv = [1,1,1]

while True:
	a = time.time()
	red   = 1
	green = 1
	blue  = 1
	
	try:
		image = ImageGrab.grab()
		
		width = image.size[0]
		height = image.size[1]
		image = image.load()
		for y in range(0, height, DECIMATE):
			for x in range(0, width, DECIMATE):
				color = image[x, y]
				red = red + color[0]
				green = green + color[1]
				blue = blue + color[2]
		red = (( red / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
		green = ((green / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
		blue = ((blue / ( (height/DECIMATE) * (width/DECIMATE) ) ) )
	
		h = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
		goal = [int(h[0] * 360), int(h[1] * 100), int(h[2] * 100)]
		bulb.set_hsv(goal[0], goal[1], goal[2])
		
		old_hsv = goal
			
	except Exception as e:
		pass

import atexit
atexit.register(lambda:bulb.stop_music())