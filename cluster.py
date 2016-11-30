import cv2
import numpy as np
import os

def cluster(in_path, out_path):

    out_path = out_path + 'cluster\\'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        
    files = os.listdir(in_path)
    
    K = 3
    attempts = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    init = cv2.KMEANS_PP_CENTERS

    for f in files:
        ext = f[-3:]
        if ext == 'JPG' or ext == 'jpg':
            print(f)
            src = cv2.imread(in_path + f)
            shape = np.shape(src)
            img = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            img = np.float32(img)
            img = cv2.GaussianBlur(img, (51,51), 0)
            img = img.reshape(shape[0] * shape[1], shape[2])

            _,labels,centers = cv2.kmeans(img, K, criteria, attempts, init)

            clustered_imgs = np.zeros((K,shape[0],shape[1],shape[2]),np.uint8)
            labels = labels.reshape(shape[0], shape[1])            
            for i in xrange(shape[0]):
                for j in xrange(shape[1]):
                    k = labels[i][j]
                    clustered_imgs[k][i][j] = src[i][j]

            for k in xrange(K):
                cv2.imwrite(out_path + f[:-4] + '_' + str(k) + '.jpg', clustered_imgs[k])

    print('Clustering finished!\n')

def main():
    in_path = raw_input('Enter folder path for raw images:\n')
    if not os.path.isdir(in_path):
        print('Invalid path!')
        return
        
    out_path = raw_input('Enter folder path for undistort images:\n')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        
    cluster(in_path, out_path)

if __name__ == "__main__":
    main()
