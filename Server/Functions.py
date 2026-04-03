#!/usr/bin/env python3
# File name   : Functions.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/04/23
import time
import threading
import json
import Ultra as ultra
import SpiderG


class Functions(threading.Thread):
	def __init__(self, *args, **kwargs):
		self.functionMode = 'none'
		self.scanList = [0,0,0]
		super(Functions, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.clear()

	def pause(self):
		self.functionMode = 'none'
		SpiderG.move_init()
		SpiderG.servoStop()
		self.__flag.clear()

	def resume(self):
		self.__flag.set()

	def automatic(self):
		self.functionMode = 'Automatic'
		self.resume()

	def distRedress(self): 
		mark = 0
		distValue = ultra.checkdist()
		while True:
			distValue = ultra.checkdist()
			if distValue > 900:
				mark +=  1
			elif mark > 5 or distValue < 900:
					break
			print(distValue)
		return round(distValue,2)

	def automaticProcessing(self):
		dist = self.distRedress()
		time.sleep(0.2)
		if dist >= 50:
			SpiderG.walk('forward')
		elif dist > 30 and dist < 50:	
			SpiderG.walk('turnleft')
			time.sleep(0.3)
			distLeft = self.distRedress()
			self.scanList[0] = distLeft
			print('left')
			SpiderG.walk('turnright')
			print('right')
			time.sleep(0.3)
			distRight = self.distRedress()
			self.scanList[1] = distRight
			print(self.scanList)

			if self.scanList[0] >= self.scanList[1]:
				SpiderG.walk('turnleft')
				time.sleep(1.3)
			else:
				SpiderG.walk('turnright')
				time.sleep(1)
		else:
			SpiderG.walk('backward')
			time.sleep(1)



	def functionGoing(self):
		if self.functionMode == 'none':
			self.pause()
		elif self.functionMode == 'Automatic':
			self.automaticProcessing()

	def run(self):
		while 1:
			self.__flag.wait()
			self.functionGoing()
			pass


if __name__ == '__main__':
	pass
	try:
		fuc=Functions()
		while True:
			fuc.automaticProcessing()
	except KeyboardInterrupt:
			pass
