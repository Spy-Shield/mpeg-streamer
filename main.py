import signal
import sys
import threading
from flask import Flask, Response

from config import server, camera
from camera import MPEGCamera
from plotter import Plotter


app     = Flask(__name__)
camera  = MPEGCamera()
plotter = Plotter(
    title='Real-Time Frame Lengths',
)

@app.route('/video')
def video():
    def generate():
        for frame in camera.stream():
            if plotter:
                plotter.update(len(frame))
            yield frame
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def signal_handler(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    def run_flask():
        app.run(host=server['host'], port=int(server['port']))
    
    with camera:
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        plotter.start()