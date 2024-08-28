import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import os
import psutil
import subprocess
import requests

def isOnline(URL):
	try:
		response = requests.get(URL, timeout=1)
		if response.status_code == 200:
			return "ONLINE"
		else:
			return f"{response.status_code}"
	except requests.exceptions.RequestException as e:
		return f"Error: {e}"

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
	shananiki_isonline = isOnline("https://shananiki.org")
	with canvas(device) as draw:
		draw.text((5, 5), f"CPU: {cpu_temp}°C", font=font, fill=255)
		draw.text((5, 15), f"Shananiki.org: {shananiki_isonline}", font=font, fill=255)

try:
	while True:
		printCPU()
		time.sleep(1.2)

except KeyboardInterrupt:
	print("Monitor stopped.")
