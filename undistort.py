import cv2
import numpy as np
import os

def undistort(calib_path, in_path, out_path):

    camera_matrix = np.loadtxt(calib_path + 'camera_matrix.txt')
    dist_coefs = np.loadtxt(calib_path + 'dist_coefs.txt')
    
    files = []
    for f in os.listdir(in_path):
        if f.endswith('.JPG') or f.endswith('.jpg'):
            files.append(f)

    out_path = out_path + 'undistort\\'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    for f in files:
        print(f)
        img = cv2.imread(in_path + f)
        img = cv2.undistort(img, camera_matrix, dist_coefs)
        cv2.imwrite(out_path + f, img)
            
    print('Undistortion finished!\n')

def main():
    calib_path = raw_input('Enter folder path for calibration parameters:\n')
    if not os.path.isdir(calib_path):
        print('Invalid path!')
        return

    in_path = raw_input('Enter folder path for raw images:\n')
    if not os.path.isdir(in_path):
        print('Invalid path!')
        return
        
    out_path = raw_input('Enter folder path for undistort images:\n')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    
    undistort(calib_path, in_path, out_path)

if __name__ == "__main__":
    main()
