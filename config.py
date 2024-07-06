import configparser

config = configparser.ConfigParser()
config.read('config.ini')

server  = config['server']
camera  = config['camera']
plotter = config['plotter']