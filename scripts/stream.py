import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2 as cv
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import platform

IS_PI = platform.machine() in ('armv7l', 'aarch64')

from src.utils.camera import Camera
camera = Camera(USE_PI_CAMERA=IS_PI)

frame_lock = threading.Lock()
current_frame = None

class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        while True:
            with frame_lock:
                if current_frame is None:
                    continue
                _, jpeg = cv.imencode('.jpg', cv.cvtColor(current_frame, cv.COLOR_BGR2RGB))
            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(jpeg.tobytes())
            self.wfile.write(b'\r\n')

def capture_loop():
    global current_frame
    while True:
        frame = camera.get_frame()
        if frame is not None:
            with frame_lock:
                current_frame = frame

t = threading.Thread(target=capture_loop, daemon=True)
t.start()

print("Stream running at http://turret.local:8080")
HTTPServer(('0.0.0.0', 8080), StreamHandler).serve_forever()