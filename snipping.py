import cv2
import numpy
import os
import argparse

ap = argparse.ArgumentParser(description = "Displays images in a given directory for cropping", 
			epilog = "Click left mouse button and then drag and release to create a rectangel. \n"
			"Repeat the operations to select a new one. \n"
			"When satisfied with the selection, press 'p' to save a positive sample, \n"
			"'n' to save a negative sample. You can select multiple positive or negative samples \n"
			"in an image. Press 'Esc' to go to the next image. Press 'Esc' twice quickly to exit.")

ap.add_argument("dir", type = str, help = "Directory to images")
args = vars(ap.parse_args())

selectObject = False
selection = [0, 0, 0, 0]
origin = [0, 0]

def onMouse(event, x, y, flags, params):
	global selectObject
	global selection
	global origin
	if selectObject:
		selection[0] = min(x, origin[0])
		selection[1] = min(y, origin[1])
		selection[2] = abs(x - origin[0])
		selection[3] = abs(y - origin[1])
		print selection

	if event == cv2.EVENT_LBUTTONDOWN:
		origin = [x, y]
		selection = [x, y, 0, 0]
		selectObject = True

	if event == cv2.EVENT_LBUTTONUP:
		selectObject = False

home = args["dir"]
os.chdir(home)
visited = []
if os.path.isfile("visited.txt"):
	with open("visited.txt", "r") as f:
		visited = f.read().splitlines()
else:
	visited.append("visited.txt")

fn = list(set(os.listdir(home)) - set(visited))

par_dir = os.path.abspath(os.path.join(home, os.pardir))
dir_p = os.path.join(par_dir, "positive")
dir_n = os.path.join(par_dir, "negative")
if not os.path.isdir(dir_p):
	os.mkdir(dir_p)

if not os.path.isdir(dir_n):
	os.mkdir(dir_n)

count_p = len(os.listdir(dir_p)) 
count_n = len(os.listdir(dir_n))

cv2.namedWindow("image", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
cv2.setMouseCallback("image", onMouse, 0)
cv2.namedWindow("cropped")

if len(fn) == 0:
	print "No more images to crop"

for f in fn:

	image = cv2.imread(f)

	while True:
		frame = image.copy()
		roi = image[selection[1]:selection[1]+selection[3], selection[0]:selection[0]+selection[2]]
		if roi.shape[0] and roi.shape[1]:
			p1 = (selection[0], selection[1])
			p2 = (selection[0]+selection[2], selection[1]+selection[3])
			cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)
			cv2.imshow("cropped", roi)

		cv2.imshow("image", frame)
		key = cv2.waitKey(100)
		if key == ord('p'):
			cv2.imwrite(os.path.join(dir_p,"p_"+str(count_p)+".jpg"), roi)
			count_p += 1
			selection = [0, 0, 0, 0]
			continue
		if key == ord('n'):
			cv2.imwrite(os.path.join(dir_n,"n_"+str(count_n)+".jpg"), roi)
			count_n +=1
			selection = [0, 0, 0, 0]
			continue
		if key == 27:
			break

	visited.append(f)
	if cv2.waitKey(1000) == 27:
		break

cv2.destroyAllWindows()

with open("visited.txt", "w") as f:
	for v in visited:
		f.write(v+"\n")
