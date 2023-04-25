from lib.models import Measurement

TOTAL_MEASUREMENTS = []


def add_measurement(measurement: Measurement) -> list[Measurement]:
    if len(TOTAL_MEASUREMENTS) > 500:
        TOTAL_MEASUREMENTS.pop(0)
    TOTAL_MEASUREMENTS.append(measurement)
    return TOTAL_MEASUREMENTS
