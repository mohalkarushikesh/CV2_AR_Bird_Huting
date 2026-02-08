import cv2
import mediapipe as mp
import numpy as np
import random
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- Load Hand Landmarker ---
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
hand_landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# Set resolution and fullscreen
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cv2.namedWindow("Finger Blaster", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Finger Blaster", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Game state
bullets = 6
score = 0
bird_x, bird_y = 50, 200
bird_speed = 5
shoot_cooldown = 0

# Track previous index finger position
prev_index_y = None

def draw_bird(frame, x, y):
    cv2.circle(frame, (x, y), 20, (0, 255, 255), -1)  # body
    cv2.circle(frame, (x+7, y-7), 5, (255, 255, 255), -1)  # eye
    cv2.circle(frame, (x+7, y-7), 2, (0, 0, 0), -1)
    pts = np.array([[x+20, y], [x+30, y-5], [x+30, y+5]], np.int32)  # beak
    cv2.fillPoly(frame, [pts], (0, 165, 255))
    cv2.ellipse(frame, (x-10, y), (15, 10), 0, 0, 360, (0, 200, 200), -1)  # wing

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    hand_result = hand_landmarker.detect(mp_image)

    # Move bird
    bird_x += bird_speed
    if bird_x > w:
        bird_x = 0
        bird_y = random.randint(100, h-100)

    draw_bird(frame, bird_x, bird_y)

    if hand_result.hand_landmarks:
        landmarks = hand_result.hand_landmarks[0]

        # Draw all landmarks in green
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        # Highlight index finger joints in red and larger
        index_points = [5, 6, 7, 8]  # MCP, PIP, DIP, TIP
        for i in index_points:
            cx, cy = int(landmarks[i].x * w), int(landmarks[i].y * h)
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        # Index finger joints
        ix, iy = int(landmarks[8].x * w), int(landmarks[8].y * h)   # tip
        px, py = int(landmarks[6].x * w), int(landmarks[6].y * h)   # pip
        tx, ty = int(landmarks[4].x * w), int(landmarks[4].y * h)   # thumb tip

        # Direction vector from PIP to TIP
        dx, dy = ix - px, iy - py
        length = np.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx, dy = dx/length, dy/length

        # Shooting only when flick detected
        if prev_index_y is not None:
            moved_up = prev_index_y - iy > 20
            thumb_extended = ty < int(landmarks[2].y * h)
            if moved_up and thumb_extended and bullets > 0 and shoot_cooldown == 0:
                bullets -= 1
                shoot_cooldown = 15

                # Compute aim line only at flick moment
                aim_end = (int(ix + dx*600), int(iy + dy*600))

                # Collision check: is bird close to aim line?
                num = abs((bird_x - ix)*(aim_end[1] - iy) - (bird_y - iy)*(aim_end[0] - ix))
                den = np.linalg.norm(np.array(aim_end) - np.array([ix, iy])) + 1e-6
                dist_to_line = num / den

                # Also check bird is in front of finger (not behind)
                dot = (bird_x - ix)*dx + (bird_y - iy)*dy
                if dist_to_line < 30 and dot > 0:
                    score += 1
                    bird_x = 0
                    bird_y = random.randint(100, h-100)

        prev_index_y = iy

        # Reload gesture (fist)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        curled = all(landmarks[tip].y > landmarks[pip].y for tip, pip in zip(finger_tips, finger_pips))
        if curled:
            bullets = 6

    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    # HUD
    cv2.putText(frame, f"Score: {score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Bullets: {bullets}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Finger Blaster", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
