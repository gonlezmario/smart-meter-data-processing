import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DATABASE_URL = str(config.get('database', 'url'))
MAX_PLOTTING_POINTS = str(config.get('database', 'max_plotting_points'))
BROKER_ADDRESS = str(config.get('mqtt', 'broker_address'))
PORT = int(config.get('mqtt', 'port'))
KEEPALIVE = int(config.get('mqtt', 'keepalive'))
TOPIC = str(config.get('mqtt', 'topic'))
EXPECTED_FREQUENCY = int(config.get('user_data', 'expected_frequency'))
