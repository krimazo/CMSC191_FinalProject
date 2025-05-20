import cv2
import numpy as np
import threading
import tkinter as tk
import random
from PIL import Image, ImageTk

# === Global variables ===
center_x = 400
game_running = False
camera_running = True
score = 0
ball_speed = [10]
life_icons = []

# === OpenCV Hand Tracking Thread ===
def track_hand():
    global center_x, camera_running

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Sets camera resolution to 640x480 px
    cap.set(3, 640)
    cap.set(4, 480)

    # Defines HSV color range for blue object detection
    lower_color = np.array([100, 150, 50])  # blue detection
    upper_color = np.array([140, 255, 255])

    while camera_running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Converts the frame from BGR to HSV (for better detection)
        mask = cv2.inRange(hsv, lower_color, upper_color) # Creates a binary mask where white = detected color, black = everything else

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea) # Selects the largest detected area
            if cv2.contourArea(c) > 1000: # Only considers objects with area > 1000 px
                x, y, w, h = cv2.boundingRect(c)
                center_x = x + w // 2 # Calculates the center x-coordinate of the detected object
                # Draws a rectangles and a dot at the object's center on the camera window
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, y + h // 2), 5, (0, 0, 255), -1)

        cv2.imshow("Object Detection Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera_running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# === Game Window and Logic ===
def start_game():
    def move_object():
        global score, game_running, lives

        if not game_running:
            return

        # Move falling object down
        canvas.move(falling_object, 0, ball_speed[0])
        pos_obj = canvas.coords(falling_object)
        pos_paddle = canvas.coords(paddle)

        # Check for catch or miss
        if pos_obj[1] >= pos_paddle[1] - 20:
            # Checks if the object's x-position is within the left and right edges of the paddle
            if pos_paddle[0] - paddle_size[0] < pos_obj[0] < pos_paddle[0] + paddle_size[0]:
                score += 1
                canvas.itemconfig(score_text, text=f"{score}")

                if score % 10 == 0:
                    ball_speed[0] += 2
                    if paddle_size[0] > 20:
                        paddle_size[0] -= 10

                reset_object()
            else:
                lose_life()

        # Ball reached bottom without catch
        elif pos_obj[1] >= 600:
            lose_life()

        # Update paddle position based on tracked x
        scaled_x = int(center_x / 640 * 800)
        new_x = max(paddle_size[0], min(scaled_x, 800 - paddle_size[0]))
        canvas.coords(paddle, new_x, 520)
        window.after(50, move_object)

    def reset_object():
        # Moves apply to a random x-position at top
        new_x = random.randint(50, 750)
        canvas.coords(falling_object, new_x, 50)

    def start_gameplay():
        global score, game_running, lives
        score = 0
        lives = 3
        ball_speed[0] = 10
        paddle_size[0] = 100
        canvas.itemconfig(score_text, text="0")
        canvas.delete("game_over")

        # Reset life icons
        for icon in life_icons:
            canvas.delete(icon)
        life_icons.clear()

        for i in range(lives):
            icon = canvas.create_image(750 - i * 30, 30, image=window.life_image)
            life_icons.append(icon)

        reset_object()
        game_running = True
        move_object()

    def lose_life():
        # Removes a heart icon and reduces life count
        global lives, game_running
        lives -= 1
        if life_icons:
            canvas.delete(life_icons.pop())
        if lives == 0:
            show_game_over()
        else:
            reset_object()

    def show_game_over():
        global game_running
        game_running = False
        canvas.create_image(0, 0, image=window.gameover_image, anchor="nw", tags="game_over")
        canvas.create_text(
            400, 395,
            text=f"Final Score: {score}",
            font=("Tiny5", 32, "bold"),
            fill="#5c5e90",
            tags="game_over"
        )

    def quit_game():
        global game_running, camera_running
        game_running = False
        camera_running = False
        window.destroy()

    # === Tkinter Window and Canvas Setup ===
    window = tk.Tk()
    window.title("Catch Me If U Cam!")
    window.geometry("800x650")

    canvas = tk.Canvas(window, width=800, height=600, bg="#87CEEB")
    canvas.pack()

    # Load and assign images
    window.bg_image = ImageTk.PhotoImage(Image.open("assets/gameBg.png"))
    window.paddle_image = ImageTk.PhotoImage(Image.open("assets/basket.png").resize((200, 200), Image.LANCZOS))
    window.ball_image = ImageTk.PhotoImage(Image.open("assets/apple.png").resize((40, 40), Image.LANCZOS))
    window.life_image = ImageTk.PhotoImage(Image.open("assets/heart.png").resize((30, 30), Image.LANCZOS))
    window.clouds_image = ImageTk.PhotoImage(Image.open("assets/clouds.png"))
    window.score_image = ImageTk.PhotoImage(Image.open("assets/score.png"))
    window.gameover_image = ImageTk.PhotoImage(Image.open("assets/gameOver.png"))

    canvas.create_image(0, 0, image=window.bg_image, anchor="nw")
    
    paddle_size = [100]
    paddle = canvas.create_image(400, 510, image=window.paddle_image)
    falling_object = canvas.create_image(200, 50, image=window.ball_image)

    canvas.create_image(0, 0, image=window.clouds_image, anchor="nw")
    canvas.create_image(0, 0, image=window.score_image, anchor="nw")
    
    score_text = canvas.create_text(145, 16, text="0", font=("Tiny5", 21), fill="#5c5e90", anchor="nw")

    lives = 3
    for i in range(lives):
        icon = canvas.create_image(750 - i * 30, 30, image=window.life_image)
        life_icons.append(icon)

    # Buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)

    start_btn = tk.Button(button_frame, text="Start", command=start_gameplay, width=10, bg="lightblue", font="Tiny5")
    start_btn.pack(side="left", padx=10)

    quit_btn = tk.Button(button_frame, text="Quit", command=quit_game, width=10, bg="lightcoral", font="Tiny5")
    quit_btn.pack(side="left", padx=10)

    window.mainloop()

# === Start camera thread and game ===
hand_thread = threading.Thread(target=track_hand, daemon=True)
hand_thread.start()

start_game()

camera_running = False
hand_thread.join()
