import cv2
import time
from config import camera

class MPEGCamera:
    def __init__(self):
        self.device = camera['device']
        self.fps = int(camera['fps'])
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.device)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.capture:
            self.capture.release()

    def get_frame(self):
        success, frame = self.capture.read()
        
        if not success:
            return None
        
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def stream(self):
        while True:
            frame = self.get_frame()
            
            if frame is None:
                break
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            time.sleep(1 / self.fps)