import configparser

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_URL = str(config.get("database", "url"))
BROKER_ADDRESS = str(config.get("mqtt", "broker_address"))
PORT = int(config.get("mqtt", "port"))
KEEPALIVE = int(config.get("mqtt", "keepalive"))
TOPIC = str(config.get("mqtt", "topic"))
EXPECTED_FREQUENCY = int(config.get("user_data", "expected_frequency"))
MAXIMUM_PLOT_POINTS = int(config.get("plotting", "maximum_plot_points"))
DELTA_T = int(config.get("plotting", "delta_t"))
PRICE_PER_KWH = float(config.get("plotting", "price_per_kwh"))
