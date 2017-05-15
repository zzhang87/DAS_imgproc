import numpy as np
import cv2
import argparse
import os

# ============================================================================

CANVAS_SIZE = (600,800)

FINAL_LINE_COLOR = (255, 255, 255)
WORKING_LINE_COLOR = (127, 127, 127)
ROW_COLOR = (255, 0, 255)
BG_COLOR = (0, 0, 255)

# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name):
        self.window_name = window_name # Name for our window

        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon


    def on_mouse(self, event, x, y, buttons, user_param):
        # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)

        if self.done: # Nothing more to do
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we're done
            print("Completing polygon with %d points." % len(self.points))
            self.done = True

    def save(self, mask):
        labeled = np.zeros((mask.shape[0], mask.shape[1], 3), np.uint8)
        for i in xrange(mask.shape[0]):
            for j in xrange(mask.shape[1]):
                if mask[i,j]:
                    labeled[i,j] = ROW_COLOR
                else:
                    labeled[i,j] = BG_COLOR

        return labeled

    def reset(self):
        self.done = False
        self.points = []

    def run(self, image):
        # Let's create our working window and set a mouse callback to handle events
        cv2.namedWindow(self.window_name, flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 800, 600)
        cv2.imshow(self.window_name, image)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse, 0)

        while True:
            while(not self.done):
                canvas = image.copy()
                # This is our drawing loop, we just continuously draw new images
                # and show them in the named window

                if (len(self.points) > 0):
                    # Draw all the current polygon segments
                    cv2.polylines(canvas, np.array([self.points]), False, FINAL_LINE_COLOR, 1)
                    # And  also show what the current segment would look like
                    cv2.line(canvas, self.points[-1], self.current, WORKING_LINE_COLOR)
                # Update the window
                cv2.imshow(self.window_name, canvas)
                # And wait 50ms before next iteration (this will pump window messages meanwhile)
                if cv2.waitKey(50) == 32: # Space hit
                    self.done = True

            # User finised entering the polygon points, so let's make the final drawing

            # of a filled polygon
            if (len(self.points) > 0):
                cv2.fillPoly(canvas, np.array([self.points]), FINAL_LINE_COLOR)
            # And show it
            cv2.imshow(self.window_name, canvas)
            # Waiting for the user to press any key
            key = cv2.waitKey()
            if key == ord('r'):
                self.reset()

            elif key == ord('s'):
                mask = cv2.fillPoly(np.zeros((image.shape[0],image.shape[1])), np.array([self.points]), 255)
                labeled = self.save(mask)
                self.reset()
                break

        return labeled

# ============================================================================

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", type = str)
    args = vars(ap.parse_args())
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
    dir_training = os.path.join(par_dir, "training")
 
    if not os.path.isdir(dir_training):
        os.mkdir(dir_training)

    os.chdir(dir_training)
    if not os.path.isdir("images"):
        os.mkdir("images")
    if not os.path.isdir("ground_truth"):
        os.mkdir("ground_truth")

    dir_img = os.path.join(dir_training, "images")
    dir_gt = os.path.join(dir_training, "ground_truth")
    img_count = len(os.listdir(dir_img))

    pd = PolygonDrawer("label")

    os.chdir(home)
    for f in fn:
        image = cv2.imread(f)
        labeled = pd.run(image)

        cv2.imwrite(os.path.join(dir_img, str(img_count)+".jpg"),image)
        cv2.imwrite(os.path.join(dir_gt, str(img_count)+".jpg"), labeled)
        img_count += 1
        visited.append(f)

        cv2.imshow("label", labeled)
        if cv2.waitKey(1000) == 27:
            break

    cv2.destroyAllWindows()
    with open("visited.txt", "w") as f:
        for v in visited:
            f.write(v+"\n")
