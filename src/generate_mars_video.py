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
    # Larger background to allow for camera shake/crop
    pad = 20
    bg_h, bg_w = height + pad*2, width + pad*2
    bg = np.zeros((bg_h, bg_w, 3), dtype=np.uint8)
    for y in range(bg_h):
        for x in range(bg_w):
            noise = random.randint(-20, 20)
            # Martian orange/red gradients
            r = min(255, max(0, 140 + noise + int(40 * math.sin(y/30.0))))
            g = min(255, max(0, 60 + noise))
            b = min(255, max(0, 20 + noise))
            bg[y, x] = [b, g, r]
    # Darker "sky" or horizon
    cv2.rectangle(bg, (0, 0), (bg_w, int(bg_h/3)), (15, 25, 50), -1)
    return bg, pad

base_bg, padding = generate_mars_bg()

# Particles for dust storm
dust_particles = []
for _ in range(100):
    dust_particles.append({
        'x': random.uniform(0, width + padding*2),
        'y': random.uniform(0, height + padding*2),
        'speed': random.uniform(5, 15),
        'size': random.randint(1, 2)
    })

aliens = []
for _ in range(3):
    x = random.randint(50, width-50)
    y = random.randint(int(height/3) + 20, height-20)
    aliens.append({'x': float(x + padding), 'y': float(y + padding), 
                   'vx': random.uniform(-1.5, 1.5), 'vy': random.uniform(-0.7, 0.7)})

for i in range(num_frames):
    # Camera shake offset
    dx = random.randint(-2, 2)
    dy = random.randint(-2, 2)
    
    # Start with a crop from the padded background
    frame_bg = base_bg[padding+dy:padding+dy+height, padding+dx:padding+dx+width].copy()
    frame = frame_bg
    
    # Draw Aliens
    for alien in aliens:
        alien['x'] += alien['vx']
        alien['y'] += alien['vy']
        
        # Simple boundary bounce
        if alien['x'] < padding or alien['x'] > width + padding: alien['vx'] *= -1
        if alien['y'] < int(height/3) + padding or alien['y'] > height + padding: alien['vy'] *= -1
        
        ax, ay = int(alien['x'] - padding - dx), int(alien['y'] - padding - dy)
        
        # Alien Body (Shadowy)
        cv2.ellipse(frame, (ax, ay), (6, 15), 0, 0, 360, (20, 25, 20), -1)
        cv2.circle(frame, (ax, ay-20), 7, (20, 25, 20), -1)
        # Moving limbs
        cv2.line(frame, (ax-3, ay-5), (ax-12 + int(6*math.sin(i/2.5)), ay+8), (20, 25, 20), 2)
        cv2.line(frame, (ax+3, ay-5), (ax+12 + int(6*math.cos(i/2.5)), ay+8), (20, 25, 20), 2)

    # Dust Storm Particles
    for p in dust_particles:
        p['x'] -= p['speed'] # Wind blowing left
        if p['x'] < 0:
            p['x'] = width + padding*2
            p['y'] = random.uniform(0, height + padding*2)
        
        px, py = int(p['x'] - padding - dx), int(p['y'] - padding - dy)
        if 0 <= px < width and 0 <= py < height:
            color = random.randint(180, 220)
            cv2.circle(frame, (px, py), p['size'], (color-100, color-50, color), -1)

    # Digital Noise / Grain
    noise = np.random.randint(0, 40, (height, width, 3), dtype=np.uint8)
    frame = cv2.add(frame, noise)
    
    # Intermittent Scanline / VHS Glitch
    if i % 15 == 0:
        glitch_y = random.randint(0, height-2)
        frame[glitch_y:glitch_y+2, :] = cv2.add(frame[glitch_y:glitch_y+2, :], 50)

    # HUD / Overlay
    if (i // fps) % 2 == 0:
        cv2.circle(frame, (25, 20), 5, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (40, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
    cv2.putText(frame, "EXT-T SIGNAL: LOW", (width-140, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    cv2.putText(frame, "2026-04-17 MARS NOBLE REGION", (10, height-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (220, 220, 220), 1)
    
    # Heavy Blur for "low-res" feel
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    out.write(frame)

out.release()
print("✓ Enhanced video generated: /home/raamuser/mars_aliens_raw.mp4")
