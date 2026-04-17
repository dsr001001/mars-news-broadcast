import cv2
import numpy as np
import random
import math

width, height = 320, 240
fps = 10
duration = 64 # rough length of the mp3
num_frames = fps * duration

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/home/raamuser/mars_aliens_raw.mp4', fourcc, fps, (width, height))

def generate_mars_bg():
    bg = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            noise = random.randint(-20, 20)
            r = min(255, max(0, 150 + noise + int(30 * math.sin(y/20.0))))
            g = min(255, max(0, 70 + noise))
            b = min(255, max(0, 30 + noise))
            bg[y, x] = [b, g, r]
    cv2.rectangle(bg, (0, 0), (width, int(height/3)), (20, 40, 80), -1)
    return bg

base_bg = generate_mars_bg()

aliens = []
for _ in range(3):
    x = random.randint(50, width-50)
    y = random.randint(int(height/3) + 20, height-20)
    aliens.append({'x': float(x), 'y': float(y), 'vx': random.uniform(-1, 1), 'vy': random.uniform(-0.5, 0.5)})

for i in range(num_frames):
    frame = base_bg.copy()
    
    for alien in aliens:
        alien['x'] += alien['vx']
        alien['y'] += alien['vy']
        
        if alien['x'] < 0 or alien['x'] > width: alien['vx'] *= -1
        if alien['y'] < int(height/3) or alien['y'] > height: alien['vy'] *= -1
        
        ax, ay = int(alien['x']), int(alien['y'])
        
        cv2.ellipse(frame, (ax, ay), (6, 15), 0, 0, 360, (50, 60, 50), -1)
        cv2.circle(frame, (ax, ay-20), 6, (50, 60, 50), -1)
        cv2.line(frame, (ax-3, ay-5), (ax-10 + int(5*math.sin(i/3.0)), ay+5), (50, 60, 50), 2)
        cv2.line(frame, (ax+3, ay-5), (ax+10 + int(5*math.cos(i/3.0)), ay+5), (50, 60, 50), 2)
        
    noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
    frame = cv2.add(frame, noise)
    
    if i % 3 == 0:
        scanline_y = (i * 5) % height
        cv2.line(frame, (0, scanline_y), (width, scanline_y), (255, 255, 255), 1)
        
    if (i // fps) % 2 == 0:
        cv2.circle(frame, (20, 20), 5, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (35, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.putText(frame, "2026-04-17 MARS SURFACE", (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    out.write(frame)

out.release()
