import logging
import time
from logging.handlers import RotatingFileHandler

from lib.mqtt_subscriber import MQTTSubscriber


class MQTTClientService:
    def __init__(self) -> None:
        self.stop_main = False

    def stop(self) -> None:
        self.stop_main = True
        mqtt_subscriber.disconnect()

    def main(self) -> None:
        while not self.stop_main:
            time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                "logs/mqtt_client_service.log", maxBytes=5_000_000, backupCount=20, mode='a'
            )
        ],
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(module)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    try:
        logging.info("Initializing MQTT Client Service...")
        service = MQTTClientService()
        logging.info("Trying to connect to the MQTT broker...")
        mqtt_subscriber = MQTTSubscriber("localhost", "smart_meter")
        mqtt_subscriber.connect()
        logging.info("Connected. Running main loop...")
        service.main()

    except KeyboardInterrupt:
        logging.info("Received stopping signal. Stopping service...")
        service.stop()

    except Exception as e:
        logging.critical(
            "Unhandled exception arisen: %s. Stopping the service..." % e)
        service.stop()
