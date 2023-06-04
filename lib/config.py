import configparser

"""
Some configurable variables accessible to the final user.
Using global variables to avoid code repetition initializing
and reading the config file with the standard python config parser.
"""

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_URL = str(config.get("database", "url"))
BROKER_ADDRESS = str(config.get("mqtt", "broker_address"))
PORT = int(config.get("mqtt", "port"))
TOPIC = str(config.get("mqtt", "topic"))
MAXIMUM_PLOT_POINTS = int(config.get("plotting", "maximum_plot_points"))
PRICE_PER_KWH = float(config.get("plotting", "price_per_kwh"))
