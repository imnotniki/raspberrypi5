import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import os
import psutil
import subprocess

def getCPUTemp():
	try:
		temp = os.popen("vcgencmd measure_temp").readline()
		return float(temp.replace("temp=", "").replace("'C\n", ""))
	except Exception as e:
		return f"Error: {e}"

serial = i2c(port=1, address=0x3c)
device = sh1106(serial)
font = ImageFont.load_default()

def printCPU():
	cpu_temp = getCPUTemp()
	with canvas(device) as draw:
		draw.text((5, 5), f"CPU: {cpu_temp}°C", font=font, fill=255)

try:
	while True:
		printCPU()
		time.sleep(1)

except KeyboardInterrupt:
	print("Monitor stopped.")
