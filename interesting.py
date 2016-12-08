import os
import cv2

def interesting(in_path):

    files = []
    for f in os.listdir(in_path):
        if f.endswith('.JPG') or f.endswith('.jpg'):
            files.append(f)
    
    os.chdir(in_path)

    if os.path.isfile('visited.txt'):
        with open('visited.txt', 'r') as f:
            visited = f.read().splitlines()

        files = list(set(files) - set(visited))

    if not files:
        print('No more images to rate.')
        return

    bingo = []
    new_visited = []

    for f in files:
        img = cv2.imread(f)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image',img)
        key = cv2.waitKey(0)
        #print key
        if key == 2490368:
            bingo.append(f)
        if key == 27:
            cv2.destroyAllWindows()
            break
        cv2.destroyWindow('image')
        new_visited.append(f)

    #print new_visited
    with open('visited.txt', 'a') as f:
        for i in new_visited:
            f.write(i+'\n')

    with open('interesting.txt', 'a') as f:
        for i in bingo:
            f.write(i+'\n')          

def main():
    print('Code for rating images as interesting or not.\n'
          'Press up arrow if the image is interesting.\n'
          'Press any other key if the image is not interesting.\n'
          'Press Esc to quit.\n')
    in_path = raw_input('Enter folder path for raw images:\n')
    if not os.path.isdir(in_path):
        print('Path does not exist!')
        return

    interesting(in_path)

if __name__ == "__main__":
    main()
