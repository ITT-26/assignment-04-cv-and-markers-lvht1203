import cv2
import numpy as np
import argparse

WINDOW_NAME = "Image Extractor"
points = []
warped = None


# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--width", type=int, required=True)
parser.add_argument("--height", type=int, required=True)
args = parser.parse_args()


# load image
original_img = cv2.imread(args.input)
if original_img is None:
    print("Could not load image")
    exit()
img = original_img.copy()
cv2.namedWindow(WINDOW_NAME)


# sort points automatically
def order_points(points):
    points = np.array(points, dtype=np.float32)
    ordered = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1)
    ordered[0] = points[np.argmin(sums)]   
    ordered[2] = points[np.argmax(sums)]  
    ordered[1] = points[np.argmin(diffs)]  
    ordered[3] = points[np.argmax(diffs)] 
    return ordered


# draw current selection
def draw_preview():
    preview = original_img.copy()
    for point in points:
        cv2.circle(preview, point, 6, (0, 0, 255), -1)
    cv2.imshow(WINDOW_NAME, preview)


# mouse click
def mouse_callback(event, x, y, flags, param):
    global warped
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            draw_preview()

            # create warped image
            if len(points) == 4:
                src = order_points(points)
                dst = np.array([
                    [0, 0],
                    [args.width - 1, 0],
                    [args.width - 1, args.height - 1],
                    [0, args.height - 1]
                ], dtype=np.float32)
                matrix = cv2.getPerspectiveTransform(src, dst)
                warped = cv2.warpPerspective(original_img, matrix,(args.width, args.height))
                cv2.imshow("Warped Result", warped)

cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
draw_preview()


# main loop
while True:

    key = cv2.waitKey(20) & 0xFF

    # ESC -> reset
    if key == 27:
        points.clear()
        warped = None
        try:
            cv2.destroyWindow("Warped Result")
        except:
            pass
        draw_preview()

    # S -> save
    elif key == ord("s") or key == ord("S"):
        if warped is not None:
            cv2.imwrite(args.output, warped)
            print("Image saved")

    # Q -> quit
    elif key == ord("q"):
        break

cv2.destroyAllWindows()