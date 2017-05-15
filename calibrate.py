import numpy as np
import cv2
import os
import sys
import argparse


class Calibrator:
    def __init__(self, mode):
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.rows = 7
        self.cols = 9
        self.size = (self.cols, self.rows)
        self.objp = np.zeros((self.rows*self.cols,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.cols,0:self.rows].T.reshape(-1,2)
        square_size = 25.6
        self.objp *= square_size
        self.objpoints = []
        self.imgpoints = []
        self.mode = mode
        self.count = 0

    def findCorners(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, self.size, None)
        if ret:
            self.count += 1
            self.objpoints.append(self.objp)

            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
            self.imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, self.size, corners, ret)
            cv2.imshow('corners',img)
            cv2.waitKey(500)

        return gray.shape[::-1]

    def calibrate(self, path = None):
        if self.mode == "image":
            os.chdir(path)
            images = []
            for f in os.listdir(path):
                if f.endswith('.JPG') or f.endswith('.jpg'):
                    images.append(f)

            for fname in images:
                img = cv2.imread(fname)
                print fname
                shape = self.findCorners(img)

        elif self.mode == "video":
            cap = cv2.VideoCapture(1)
            while self.count < 25 and cap.grab():
                _, img = cap.retrieve()
                shape = self.findCorners(img)

        else:
            raise Exception("Unknown mode")

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,
                                                shape, None, None)

        np.savetxt('camera_matrix.txt', mtx)
        np.savetxt('dist_coefs.txt', dist)

        cv2.destroyAllWindows()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", type = str,
                    help = "'video' or 'image'")
    ap.add_argument("-d", "--dir", type = str,
                    help = "Directory to images")
    args = vars(ap.parse_args())

    calib = Calibrator(args["mode"])
    calib.calibrate(args["dir"])

if __name__ == "__main__":
    main()