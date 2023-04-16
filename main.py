import logging
import time
from logging.handlers import RotatingFileHandler

from lib.compute_powers import ComputePowers
from lib.models import Measurement
from lib.mqtt_subscriber import MQTTSubscriber
from lib.plotting import update_plot


class MQTTClientService:
    def __init__(self) -> None:
        self.stop_main = False
        self.mqtt_subscriber = MQTTSubscriber(
            broker_address="localhost", port=1883, topic="smart_meter")

    def stop(self) -> None:
        self.stop_main = True
        self.mqtt_subscriber.disconnect()

    def main(self) -> None:

        logging.info("Connecting to the MQTT broker...")
        self.mqtt_subscriber.connect()

        logging.info("Querying last measurements...")
        measurements = Measurement.query_latest_measurements()

        logging.info("Computing powers...")
        processed_data = ComputePowers(measurements=measurements)

        logging.info("Plotting results...")
        update_plot(processed_data=processed_data)

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
        service.main()

    except KeyboardInterrupt:
        logging.info("Received stopping signal. Stopping service...")
        service.stop()

    except Exception as e:
        logging.critical(
            "Unhandled exception arisen: %s. Stopping the service..." % e)
        service.stop()
