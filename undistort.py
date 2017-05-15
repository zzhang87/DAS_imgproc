import cv2
import numpy as np
import os

def undistort(calib_path, in_path, out_path):

    camera_matrix = np.loadtxt(os.path.join(calib_path, 'camera_matrix.txt'))
    dist_coefs = np.loadtxt(os.path.join(calib_path, 'dist_coefs.txt'))
    
    files = []
    for f in os.listdir(in_path):
        if f.endswith('.JPG') or f.endswith('.jpg'):
            files.append(f)

    out_path = os.path.join(in_path, 'undistort')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    print('Undistorting images:\n')
    for f in files:
        print(f)
        img = cv2.imread(os.path.join(in_path, f))
        img = cv2.undistort(img, camera_matrix, dist_coefs)
        cv2.imwrite(os.path.join(out_path, f), img)
            
    print('Undistortion finished!\n')

def main():
    calib_path = raw_input('Enter folder path for calibration parameters:\n')
    if calib_path == '':
        calib_path = '/home/zzhang52/Research/DAS_imgproc'
    if not os.path.isdir(calib_path):
        print('Invalid path!')
        return

    in_path = raw_input('Enter folder path for raw images:\n')
    if not os.path.isdir(in_path):
        print('Invalid path!')
        return
        
    out_path = raw_input('Enter folder path for output images:\n')
    if out_path == '':
        out_path = os.path.join(in_path, 'undistort')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    
    undistort(calib_path, in_path, out_path)

if __name__ == "__main__":
    main()