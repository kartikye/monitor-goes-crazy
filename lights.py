
from yeelight.transitions import *
from yeelight import Flow, Bulb

bulb = Bulb("10.226.239.115",effect="smooth", duration=100)

from PIL import ImageGrab
import time
import os
from colour import Color
import colorsys

DECIMATE = 10

o_r = 0
o_g = 0
o_b = 0

last = time.time()

bucket = 60

rate_last_time = time.time()
rate_last_count = bucket

state = False

print("start")
bulb.start_music()
bulb.stop_music()

def change_state():
	global state
	print(state)
	try:
		if state:
			bulb.stop_music()
			print("normal mode")
			bucket = 60
			state = not state
		else:
			bulb.start_music()
			print("music mode")
			state = not state
	except Exception as e:
		print('hi')
		print(e)


while True:
	
	red   = 1
	green = 1
	blue  = 1
	
	image = ImageGrab.grab()  # take a screenshot

	for y in range(0, image.size[1], DECIMATE):  #loop over the height
		for x in range(0, image.size[0], DECIMATE):  #loop over the width
			color = image.getpixel((x, y))  #grab a pixel
			red = red + color[0]
			green = green + color[1]
			blue = blue + color[2]
	red = (( red / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )
	green = ((green / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )
	blue = ((blue / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )

	if (abs(red - o_r) > 5 or abs(green - o_g) > 5 or abs(blue - o_b) > 5):
		try:
			if bucket < 1 and not state:
				change_state()
			
			bucket -= 1
			print("-1", bucket)
			h = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
			bulb.set_hsv(int(h[0]*360), int(h[1]*100), int(h[2]*100))
				
				
		except Exception as e:
			if '-1' in str(e):
				change_state()
		o_r = red
		o_b = blue
		o_g = green


	if time.time() - last > 2:
		last = time.time()
		if bucket < 60:
			bucket += 1
			print("+1",bucket)

	if time.time() - rate_last_time > 5:
		rate = abs(bucket - rate_last_count)/(time.time() - rate_last_time)
		if rate < 2 and state:
			change_state()
		elif rate > 3 and not state:
			change_state()



import atexit
atexit.register(lambda:bulb.stop_music())