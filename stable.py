import cv2
import numpy as np
import os
import argparse

class Stablizer:
	def __init__(self, frame):
		self.frame = frame
		self.height, self.width, self.depth = frame.shape

		self.X = np.zeros(3, dtype = float)
		self.X_ = np.zeros(3, dtype = float)
		self.P = np.ones(3, dtype = float)
		self.P_ = np.zeros(3, dtype = float)
		self.K = np.zeros(3, dtype = float)
		self.z = np.zeros(3, dtype = float)

		self.pstd = 4e-3
		self.cstd = 1.5

		self.Q = self.pstd * np.ones(3, dtype = float)
		self.R = self.cstd * np.ones(3, dtype = float)

		self.state = np.zeros(3, dtype = float)
		self.dX = np.zeros(3, dtype = float)
		self.M = None
		self.good_M = None

	def estimateTransform(self, new_frame):
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
		corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 30)
		new_corners, stats, err = cv2.calcOpticalFlowPyrLK(gray, new_gray, corners, None)

		self.M = cv2.estimateRigidTransform(corners, new_corners, False)

		if not self.M is None:
			self.good_M = self.M

		else:
			self.M = self.good_M

		self.dX[0] = self.M[0,2]
		self.dX[1] = self.M[1,2]
		self.dX[2] = np.arctan2(self.M[1,0], self.M[0,0])

		self.state += self.dX

	def smoothTrajectory(self):
		self.X_ = self.X
		self.P_ = self.P + self.Q
		self.K = self.P_ / (self.P_ + self.R)
		self.X = self.X_ + self.K * (self.state - self.X_)
		self.P = (np.ones(3, dtype = float) - self.K) * self.P_

		self.dX += self.X - self.state

	def updateTransform(self):
		self.M[0,0] = np.cos(self.dX[2])
		self.M[0,1] = -np.sin(self.dX[2])
		self.M[1,0] = np.sin(self.dX[2])
		self.M[1,1] = np.cos(self.dX[2])
		self.M[0,2] = self.dX[0]
		self.M[1,2] = self.dX[1]

	def transformFrame(self):
		new_frame = cv2.warpAffine(self.frame, self.M, (self.width, self.height))
		return new_frame

	def stablize(self, new_frame):
		self.estimateTransform(new_frame)
		self.smoothTrajectory()
		self.updateTransform()
		stable_frame = self.transformFrame()
		self.frame = new_frame

		return stable_frame


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("video", type = str, help = "video file to stablize")
	args = vars(ap.parse_args())

	print args["video"]
	cap = cv2.VideoCapture(args["video"])
	assert(cap.isOpened())

	_, frame = cap.read()

	st = Stablizer(frame)

	cv2.namedWindow("stable", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
	while cap.grab():
		_, frame = cap.retrieve()
		stable_frame = st.stablize(frame)

		cv2.imshow("stable", stable_frame)

		if cv2.waitKey(10) == 27:
			break

	cv2.destroyAllWindows()
	cap.release()


if __name__ == "__main__":
	main()
