import logging
import time
from logging.handlers import RotatingFileHandler


class MQTTClientService:
    def __init__(self) -> None:
        self.stop_main = False

    def stop(self) -> None:
        self.stop_main = True

    def main(self) -> None:
        while not self.stop_main:
            pass
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
        logging.critical("Unhandled exception arisen. Stopping the service...")
        service.stop()
