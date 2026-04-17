# Mars Breaking News Broadcast Generator

This project automates the creation of a realistic, multi-media breaking news broadcast. It was developed to simulate an emergency breaking news report of humanity finding extraterrestrial life on Mars. 

The pipeline dynamically performs the following steps:
1. **Text-to-Speech (TTS):** Generates high-quality, neural Hindi speech (`edge-tts`) from a provided text file.
2. **Audio Mixing:** Mixes the news narration with royalty-free background music, adjusting volumes to create an authentic "news broadcast" atmosphere.
3. **Procedural Video Generation:** Uses OpenCV to algorithmically render a "found footage" style low-resolution video (320x240) of the Martian surface complete with static noise, scanlines, and moving alien shapes.
4. **Multiplexing:** Combines the generated audio and video into a compact MP4 file using `ffmpeg`.
5. **Distribution:** Emails the final `.mp4` attachment securely to a designated operator email address using SMTP.

## Directory Structure
- `src/mars_news.txt`: The raw text of the news report in Hindi.
- `src/generate_mars_video.py`: OpenCV script for creating the "found footage" Martian surface.
- `src/send_email.py`: SMTP-based script that safely packages and sends the final mp4 artifact via email.

## Prerequisites
You need the following installed:
- Python 3
- `ffmpeg` (for media multiplexing)
- `edge-tts`
- `opencv-python-headless`
- `numpy`

## Usage
1. Provide the news script.
2. Run TTS using Edge TTS.
3. Mix audio streams with `ffmpeg`.
4. Generate video via `python3 generate_mars_video.py`.
5. Multiplex and dispatch.

*Disclaimer: This is a fictional demonstration project combining multiple AI/Multimedia techniques into an automated workflow.*