import logging
import threading
import time
from logging.handlers import RotatingFileHandler

from lib.compute_powers import ComputePowers
from lib.models import Measurement
from lib.mqtt_subscriber import MQTTSubscriber
from lib.plotting import DataPlot


class MQTTClientService:
    def __init__(self) -> None:
        self.stop_main = False
        self.mqtt_subscriber = MQTTSubscriber(
            broker_address="localhost", port=1883, topic="smart_meter")
        self.mqtt_thread = threading.Thread(
            target=self.mqtt_subscriber.connect)
        self.mqtt_thread_started = False

    def stop(self) -> None:
        self.stop_main = True
        logging.info("Disconnecting from the MQTT broker...")
        self.mqtt_subscriber.disconnect()
        logging.info("Joining MQTT Subscriber thread...")
        self.mqtt_thread.join()

    def main(self) -> None:

        while not self.stop_main:
            if not self.mqtt_thread_started:
                logging.info("Starting thread for the MQTT broker...")
                self.mqtt_thread.start()
                self.mqtt_thread_started = True

            logging.info("Querying last measurements...")
            measurements_to_plot = Measurement.query_latest_measurements()

            logging.info("Computing powers...")
            processed_data = []

            for measurement in measurements_to_plot:
                measurement_point = ComputePowers(measurement=measurement)
                processed_data.append(measurement_point)

            logging.info("Plotting results...")
            data_plot = DataPlot(processed_data=processed_data)
            data_plot.plot_data()
            time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                "logs/mqtt_client_service.log",
                maxBytes=5_000_000,
                backupCount=20,
                mode='a'
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
        logging.critical(
            "Unhandled exception arisen: %s. Stopping the service..." % e)
        service.stop()
