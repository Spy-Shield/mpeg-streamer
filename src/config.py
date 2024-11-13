import time
import configparser
import uuid
from src.singleton import singleton


@singleton
class MainConfig:
    def __init__(self, main):
        self.host = main['host']
        self.port = main.getint('port')


@singleton
class PlotterConfig:
    def __init__(self, plotter):
        self.show = plotter.getboolean('show')
        self.span = plotter.getint('span')


@singleton
class CameraConfig:
    def __init__(self, wire):
        self.device = wire['device']
        self.fps = wire.getint('fps')


@singleton
class MPEGStreamerConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.__session = uuid.uuid4()

        self.time = time.time()
        self.main = MainConfig(self.config['main'])
        self.plotter = PlotterConfig(self.config['plotter'])
        self.camera = CameraConfig(self.config['camera'])

    @property
    def session(self):
        return self.__session

    def to_dick(self):
        streamer = self.__dict__.copy()
        main = self.main.__dict__.copy()
        plotter = self.plotter.__dict__.copy()
        camera = self.camera.__dict__.copy()

        streamer['main'] = main
        streamer['plotter'] = plotter
        streamer['camera'] = camera

        return streamer


config = MPEGStreamerConfig()
