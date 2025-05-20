# Catch Me If U Cam
Catch Me If U Cam is a motion-controlled object-catching game made with Python, OpenCV, and Tkinter.
Move a blue-colored object in front of your webcam to control the basket and catch falling apples on screen. The game tracks your score and lives, increasing difficulty as you play.
### Features:
+ Real-time color tracking using OpenCV
+ Motion-controlled game where you move a **blue-colored object** to catch apples
+ Increasing difficulty as score increases
+ Smooth integration of computer vision and a graphical game interface
### Dependencies:
+ Python 3.x
+ OpenCV (`opencv-python`)
+ Pillow (`PIL`)
+ NumPy
### Installation:
Open your terminal and run:\
`pip install opencv-python pillow numpy`
### How to Run:
1. Clone or download this repositor.
2. Ensure you have **Python 3.x** installed.
3. Open a terminal in the project directory.
4. Run the program with:
`python game.py`
5. Allow access to your webcam if prompted.
6. Move a blue-colore object in front of your camera to control the basket.
7. Click Start to begin, and Quit to properly close the program.
### Notes and Limitations
+ The program requires good lighting for reliable color detection.
+ Make sure your webcam is connected and working.
+ If your the program multiple times without restarting your IDE (e.g. VS Code), the camera might not release properly.
    + To fix this: restart your terminal or VS Code before running again.
 ### Assets
All image and font assets are stored inside the `assets` folder\
\
Developed for **CMSC 191: Computer Vision in Python**\
by: **Kristianna Isabel R. Mazo**\
This project is for educational purposes.
