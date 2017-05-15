import pandas as pd
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import undistort
import argparse
import shutil

def mosaic(in_path, overlap):

	os.chdir(in_path)
	filename = 'location.txt'
	log = pd.read_csv(filename, sep = ' ')
	log = log.sort_values(['#name'])

	fn = list(log['#name'])
	Y = np.asarray(log['latitude/Y'])
	X = np.asarray(log['longitude/X'])
	# plt.plot(X,Y, marker='*', ls = 'None')
	# plt.show()

	X_max = np.max(X)
	X_min = np.min(X)

	Y_max = np.max(Y)
	Y_min = np.min(Y)

	dY = np.max(abs(np.diff(Y)))
	dX = np.max(abs(np.diff(X)))

	rows = int( round((Y_max-Y_min)/dY) ) + 1
	cols = int( round((X_max-X_min)/dX) ) + 1

	img = cv2.imread(log['#name'][0])
	size = np.shape(img)

	R = size[0] + (rows - 1) * (int)((1 - overlap) * size[0])
	C = size[1] + (cols - 1) * (int)((1 - overlap) * size[1])

	canvas = np.zeros((R,C,size[2]), dtype = np.uint8)

	os.chdir(os.path.join(in_path, 'undistort'))

	for i in xrange(len(fn)):
		img = cv2.imread(fn[i])
		row = int( round((Y_max-Y[i])/dY) )
		col = int( round((X[i]-X_min)/dX) )
		r_start = row * (int)((1 - overlap) * size[0])
		r_end = r_start + size[0]
		c_start = col * (int)((1 - overlap) * size[1])
		c_end = c_start + size[1]
		canvas[r_start:r_end, c_start:c_end, :] = img

	small = cv2.resize(canvas, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
	cv2.namedWindow('mosaic', cv2.WINDOW_AUTOSIZE)
	cv2.imshow('mosaic', small)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imwrite('../mosaic.jpg', canvas)
	cv2.imwrite('../mosaic_small.jpg', small)

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--calib", type = str, required = True, 
					help = "Path to calibration files (camera matrix and distortion coefficient)")
	ap.add_argument("-i", "--input", type = str, required = True,
					help = "Path to input files")
	ap.add_argument("-o", "--output", type = str, default = "",
					help = "Path to output files (omit if same as input)")
	ap.add_argument("overlap", type = float,
					help = "Percentage of overlap in decimal")
	args = vars(ap.parse_args())

	calib_path = args["calib"]

	if not os.path.isdir(calib_path):
	    print('Invalid calibration path!')
	    return

	in_path = args["input"]
	if not os.path.isdir(in_path):
	    print('Invalid input path!')
	    return
	    
	out_path = args["output"]
	if out_path == "":
	    out_path = os.path.join(in_path, 'undistort')
	if not os.path.isdir(out_path):
	    os.mkdir(out_path)
	else:
		shutil.rmtree(out_path)

	overlap = args["overlap"]

	undistort.undistort(calib_path, in_path, out_path)
	mosaic(in_path, overlap)

if __name__ == "__main__":
    main()
