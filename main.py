import signal
import sys
import threading
from flask import Flask, Response

from src.logger import logger
from src.config import config
from src.plotter import plotter
from src.camera import MPEGCamera

app = Flask(__name__)
camera = MPEGCamera()


def generate():
    for frame in camera.stream():
        if plotter:
            plotter.update(len(frame))
        yield frame


@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def signal_handler(sig, frame):
    if config.plotter.show:
        plotter.root.quit()

    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    logger.info(f'MPEGStreamer session started: {config.session}')
    logger.debug(config.to_dick())


    def run():
        app.run(host=config.main.host, port=config.main.port)


    with camera:
        if config.plotter.show:
            flask_thread = threading.Thread(target=run)
            flask_thread.daemon = True
            flask_thread.start()
            plotter.start()
        else:
            run()
