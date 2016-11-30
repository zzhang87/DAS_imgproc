import numpy as np
import cv2
import os

def find_contour(in_path, out_path): 
    
    out_path = out_path + 'contour\\'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        
    output = open(out_path + 'boxes.txt', 'w')
    files = os.listdir(in_path)
    files.sort()

    kernel_size = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    it = 3
    thresh = 10
    currID = ''

    for f in files:
        ext = f[-3:]
        if ext == 'JPG' or ext == 'jpg':
            print(f)
            img = cv2.imread(in_path + f)
            img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations = it)
            img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations = it)
            imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, imgray = cv2.threshold(imgray, thresh, 255, 0)
            contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(img,contours,-1,(0,255,0),3)
            if f[:-6] != currID:
                output.write('\n')
                output.write(f[:-6] + '\n')
                currID = f[:-6]
            for i in range (len(contours)):
                x,y,w,h = cv2.boundingRect(contours[i])
                temp = ','.join(str(x) for x in [x,y,w,h])
                output.write(temp+'\n')
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite(out_path + f, img)
    output.close()
    print('Finding contours finished!\n')

def main():
    in_path = raw_input('Enter folder path for raw images:\n')
    if not os.path.isdir(in_path):
        print('Invalid path!')
        return
        
    out_path = raw_input('Enter folder path for undistort images:\n')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        
    find_contour(in_path, out_path)

if __name__ == "__main__":
    main()
