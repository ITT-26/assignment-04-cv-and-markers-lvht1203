import cv2
import numpy as np
import random

# image source: https://www.flaticon.com/free-icon/orange_1728765
orange_img = cv2.imread(
    "images/orange.png",
    cv2.IMREAD_UNCHANGED
)
orange_img = cv2.resize(
    orange_img,
    (70, 70)
)
# image source: https://www.flaticon.com/free-icon/shopping-basket_3142740
basket_img = cv2.imread(
    "images/basket.png",
    cv2.IMREAD_UNCHANGED
)
basket_img = cv2.resize(
    basket_img,
    (100, 100)
)

def make_orange(width, height):
    return {
        "x": random.randint(60, width - 60),
        "y": random.randint(-300, -50),
        "speed": random.randint(3, 6),
        "radius": 30
    }


def detect_red_cursor(img):
    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )
    mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )
    mask = mask1 + mask2
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return None
    largest = max(
        contours,
        key=cv2.contourArea
    )
    area = cv2.contourArea(largest)
    if area < 300:
        return None
    x, y, w, h = cv2.boundingRect(largest)
    return (
        x + w // 2,
        y + h // 2
    )

# blend png image with webcam frame
# AI-assisted implementation
def draw_orange(img, orange):
    x = int(orange["x"])
    y = int(orange["y"])
    h, w = orange_img.shape[:2]
    top_left_x = x - w // 2
    top_left_y = y - h // 2

    # keep image inside frame
    if top_left_x < 0 or top_left_y < 0:
        return
    if top_left_x + w > img.shape[1]:
        return
    if top_left_y + h > img.shape[0]:
        return

    # split channels
    bgr = orange_img[:, :, :3]
    alpha = orange_img[:, :, 3] / 255.0
    roi = img[
        top_left_y:top_left_y + h,
        top_left_x:top_left_x + w
    ]
    # blend png
    for c in range(3):
        roi[:, :, c] = (
            alpha * bgr[:, :, c] +
            (1 - alpha) * roi[:, :, c]
        )
        
# AI-assisted png overlay rendering
def draw_basket(img, x, y):
    h, w = basket_img.shape[:2]
    top_left_x = x - w // 2
    top_left_y = y - h // 2
    if top_left_x < 0 or top_left_y < 0:
        return
    if top_left_x + w > img.shape[1]:
        return
    if top_left_y + h > img.shape[0]:
        return
    bgr = basket_img[:, :, :3]
    alpha = basket_img[:, :, 3] / 255.0
    roi = img[
        top_left_y:top_left_y + h,
        top_left_x:top_left_x + w
    ]
    for c in range(3):
        roi[:, :, c] = (
            alpha * bgr[:, :, c] +
            (1 - alpha) * roi[:, :, c]
        )