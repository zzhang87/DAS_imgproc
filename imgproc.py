import undistort
import cluster
import find_contour
import os

def main():
    
    calib_path = raw_input('Enter folder path for calibration parameters:\n')
    if not os.path.isdir(calib_path):
        print('Invalid path!')
        return
        
    in_path = raw_input('Enter folder path for input images:\n')
    if not os.path.isdir(in_path):
        print('Invalid path!')
        return
            
    out_path = raw_input('Enter folder path for output images:\n')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    
    undistort.undistort(calib_path, in_path, out_path)

    cluster.cluster(out_path+'undistort\\', out_path)
    
    find_contour.find_contour(out_path+'cluster\\', out_path)

if __name__ == "__main__":
    main()
