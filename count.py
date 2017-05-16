import cv2
import numpy as np
import random
import os
import argparse

class Counter:
	def __init__(self):
		self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
		cv2.namedWindow("green", cv2.WINDOW_NORMAL)
		
	def ExGreen(self, img):
		temp = img.astype(np.float32)
		green = 2 * temp[:,:,1] - temp[:,:,0] - temp[:,:,2]
		green = np.clip(green, 0, 255)
		green = green.astype(np.uint8)
		ret, seg = cv2.threshold(green, 50, 255, cv2.THRESH_BINARY)
		
		cv2.imshow("green", seg)
		cv2.waitKey()
		
		return seg

	def H_value_seg(self, img):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		low_b = np.array([25,100,100])
		up_b = np.array([70,255,255])
		seg = cv2.inRange(hsv, low_b, up_b)

		return seg

	def Template_match(self, img, temp):
		match = cv2.matchTemplate(img, temp, cv2.TM_CCORR_NORMED)
		ret, seg = cv2.threshold(result, 0.8, 255, cv2.THRESH_BINARY_INV)
		seg = cv2.convertScaleAbs(seg)

		return seg
		
	def count(self, img):
		seg = self.ExGreen(img)
		seg = cv2.morphologyEx(seg, cv2.MORPH_OPEN, self.kernel, iterations = 2)
		seg = cv2.morphologyEx(seg, cv2.MORPH_CLOSE, self.kernel, iterations = 1)
		cv2.imshow("green", seg)
		cv2.waitKey()
		
		contours = cv2.findContours(seg, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		color = cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR)
		cv2.drawContours(color, contours[1], -1, (0, 0, 255), 3)
		cv2.imshow("green", color)
		cv2.waitKey()
		
		return len(contours[1])

    
def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("image")
	args = vars(ap.parse_args())
	
	image = cv2.imread(args["image"])
	counter = Counter()
	print "Count:", counter.count(image)
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	main()
