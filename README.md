# CV2_AR_Bird_Huting

## Finger Blaster: Bird Hunt AR 🎯🐦

Finger Blaster is a gesture‑controlled arcade game where your **hand becomes the gun**.  
Using the **MediaPipe Hand Landmarker**, the game tracks your index finger direction and draws a laser line to aim at cartoon birds flying across the screen.  
A dramatic **finger flick upward** fires a shot, while making a **fist reloads your gun** with 6 bullets.  
Score points by hitting birds with precise laser shots and enjoy the mix of computer vision with classic shooting gameplay.

---

## ✨ Features
- Real‑time hand tracking with MediaPipe Tasks API.  
- Laser line follows the **actual pointing direction** of your index finger.  
- Flick gesture to shoot, fist gesture to reload.  
- Cartoon birds with simple animations.  
- Score and bullet counter displayed on screen.  
- Fullscreen gameplay for immersive experience.

---

## 🎮 How to Play
1. Start the game — a bird will fly across the screen.  
2. Point your **index finger** like a gun; a red laser shows your aim.  
3. Flick your index finger upward with thumb extended → **shoot**.  
4. You have **6 bullets**; make a **fist** to reload.  
5. Hit birds with your laser shots to increase your score.  

---

## 🛠️ Requirements
- Python 3.9+  
- OpenCV (`pip install opencv-python`)  
- MediaPipe (`pip install mediapipe`)  
- A webcam  

---

## 🚀 Run the Game
```bash
python hand_gun_game.py
