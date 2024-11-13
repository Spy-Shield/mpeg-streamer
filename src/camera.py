import cv2
import time
from src.config import config


class MPEGCamera:
    def __init__(self):
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(config.camera.device)
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

            time.sleep(1 / config.camera.fps)
