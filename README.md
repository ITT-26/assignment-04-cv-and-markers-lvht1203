# Assignment 04 - CV and Markers

## Requirements

Install the required libraries:

```bash
pip install opencv-python numpy
```

For ArUco marker support:

```bash
pip install opencv-contrib-python
```

---

# Task 1 - Perspective Transformation

## Run

```bash
python image_extractor.py input.jpg output.jpg --width 800 --height 600
```

Example:

```bash
python image_extractor.py perspective_transformation/sample_image.jpg perspective_transformation/output.jpg --width 800 --height 600
```

---

## Controls

* Left click four corner points on the image
* Press `S` to save the transformed image
* Press `ESC` to reset/discard

---

## Notes

* The four points can be selected in any order
* The program automatically sorts the points before applying the perspective transformation
* Visual feedback is shown after selecting points

---

# Task 2 - AR Orange Catching Game

## Run

```bash
python AR_game.py
```

---

## How to Play

* Show the white AR board with the 4 ArUco markers to the webcam
* Use a red object as the cursor
* Move the basket to catch the falling oranges
* Each caught orange increases the score
* The game ends after missing 5 oranges

---

## Notes

* The AR board should stay as still as possible for smooth gameplay
* The oranges and basket disappear when the markers are no longer detected
* The game reappears automatically once all 4 markers are visible again
* Press `Q` to quit the game

---

## Image Sources

Orange icon:
https://www.flaticon.com/free-icon/orange_1728765

Basket icon:
https://www.flaticon.com/free-icon/shopping-basket_3142740

