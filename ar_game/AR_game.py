import cv2
import numpy as np

from aruco_utils import (get_perspective_matrix, detector, order_points)
from game_utils import (make_orange, draw_orange, draw_basket, detect_red_cursor)


# camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
WIDTH = 640
HEIGHT = 480


# game variables
score = 0
misses = 0
max_misses = 5
game_over = False
matrix = None


# oranges
oranges = []

for i in range(3):
    oranges.append(make_orange(WIDTH, HEIGHT))


# main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    display = frame.copy()

    # convert webcam frame to grayscale for marker detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    # marker visible
    if ids is not None and len(corners) >= 4:
        marker_points = []
        for corner in corners[:4]:
            pts = corner[0]
            center_x = int(np.mean(pts[:, 0]))
            center_y = int(np.mean(pts[:, 1]))
            marker_points.append([center_x, center_y])
        marker_points = order_points(marker_points)
        target_points = np.array([
            [0, 0],
            [WIDTH - 1, 0],
            [WIDTH - 1, HEIGHT - 1],
            [0, HEIGHT - 1]
        ], dtype=np.float32)
        matrix = cv2.getPerspectiveTransform(marker_points, target_points)
    # marker lost
    else:
        matrix = None

    # game
    if matrix is not None:
        display = cv2.warpPerspective(frame, matrix, (WIDTH, HEIGHT))
        cursor = detect_red_cursor(display)
        if cursor is not None:
            cursor_x, cursor_y = cursor
            draw_basket(display, cursor_x, cursor_y)
        if not game_over:
            for orange in oranges:
                orange["y"] += orange["speed"]
                draw_orange(display, orange)
                # collision
                if cursor is not None:
                    dx = cursor_x - orange["x"]
                    dy = cursor_y - orange["y"]
                    distance = np.sqrt(dx * dx + dy * dy)
                    if distance < orange["radius"] + 15:
                        score += 1
                        orange.clear()
                        orange.update(make_orange(WIDTH, HEIGHT))
                # missed orange
                if orange["y"] > HEIGHT + 40:
                    misses += 1
                    orange.clear()
                    orange.update(make_orange(WIDTH, HEIGHT))
                    if misses >= max_misses:
                        game_over = True

        # AI-assisted: simple game UI text
        # score
        cv2.putText(
            display,
            "Score: " + str(score),
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # misses
        cv2.putText(
            display,
            "Misses: " + str(misses) + "/5",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # game over
        if game_over:

            cv2.putText(
                display,
                "GAME OVER",
                (140, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 0, 255),
                4
            )

            cv2.putText(
                display,
                "Final Score: " + str(score),
                (150, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                3
            )

    else:

        cv2.putText(
            display,
            "Show 4 markers",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
    cv2.imshow("AR Game", display)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()