import logging
import threading
import time
from logging.handlers import RotatingFileHandler

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from lib.compute_powers import ProcessedMeasurement
from lib.models import Measurement
from lib.mqtt_subscriber import MQTTSubscriber
from lib.plotting import Plotter


class MQTTClientService:
    def __init__(self) -> None:
        self.stop_main = False
        self.mqtt_subscriber = MQTTSubscriber(
            broker_address="localhost", port=1883, topic="smart_meter"
        )
        self.mqtt_thread = threading.Thread(target=self.mqtt_subscriber.connect)
        self.mqtt_thread_started = False
        self.plotter = Plotter()

    def stop(self) -> None:
        self.stop_main = True
        logging.info("Disconnecting from the MQTT broker...")
        self.mqtt_subscriber.disconnect()
        logging.info("Joining MQTT Subscriber thread...")
        self.mqtt_thread.join()
        self.plotter.close_figures()

    def main(self) -> None:
        while not self.stop_main:
            if not self.mqtt_thread_started:
                logging.info("Starting thread for the MQTT broker...")
                self.mqtt_thread.start()
                self.mqtt_thread_started = True

            if self.mqtt_subscriber.is_connected:
                logging.debug("Querying last measurements...")
                latest_measurements = Measurement.query_latest_measurements()

                logging.debug("Computing powers...")
                measurement_point = ProcessedMeasurement(
                    measurements=latest_measurements
                )

                logging.debug("Plotting results...")
                self.plotter.update(
                    measurement_point=measurement_point.get_all_measurement_attributes()
                )
            time.sleep(0.3)


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                "logs/service.log",
                maxBytes=5_000_000,
                backupCount=20,
                mode="a",
            )
        ],
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d in %(funcName)s(): %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    service = MQTTClientService()

    try:
        logging.info("Initializing MQTT Client Service...")
        service.main()

    except KeyboardInterrupt:
        logging.info("Received stopping signal. Stopping service...")
        service.stop()

    except Exception as e:
        logging.critical("Unhandled exception arisen: %s. Stopping the service..." % e)
        service.stop()
