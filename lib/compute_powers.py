from lib.models import Measurement

last_measurements = Measurement.query_latest_measurements()

for measurement in last_measurements:
    print(measurement.voltage_1)
