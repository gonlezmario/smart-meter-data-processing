import numpy as np
from scipy.optimize import curve_fit

from lib.models import Measurement


class ModelSignals:
    def __init__(self) -> None:
        last_measurements = Measurement.query_latest_measurements()

        self.voltage_1_data_points = []
        self.voltage_2_data_points = []
        self.voltage_3_data_points = []
        self.current_1_data_points = []
        self.current_2_data_points = []
        self.current_3_data_points = []

        for measurement in last_measurements:
            self.voltage_1_data_points.append(measurement.voltage_1)
            self.voltage_2_data_points.append(measurement.voltage_2)
            self.voltage_3_data_points.append(measurement.voltage_3)
            self.current_1_data_points.append(measurement.current_1)
            self.current_2_data_points.append(measurement.current_2)
            self.current_3_data_points.append(measurement.current_3)

        self.data_set_length = len(self.last_measurements)
        self.timestamp_n = np.linspace(0, 1, self.data_set_length)

    def sine_signal(x, frequency, amplitude, phase, offset):
        return amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset

    def get_voltage_signals(self):
        frequency_guess = 50  # Hz
        amplitude_guess = 220  # V
        phase_guess = 0  # radians
        offset_guess = 0  # V
        initial_guess = [frequency_guess,
                         amplitude_guess, phase_guess, offset_guess]

        voltage_1_signal, voltage_1_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.voltage_1_data_points, p0=initial_guess)
        voltage_2_signal, voltage_2_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.voltage_2_data_points, p0=initial_guess)
        voltage_3_signal, voltage_3_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.voltage_3_data_points, p0=initial_guess)

        return voltage_1_signal, voltage_2_signal, voltage_3_signal

    def get_current_signals(self):
        frequency_guess = 50  # Hz
        amplitude_guess = 15  # A
        phase_guess = 0  # radians
        offset_guess = 0  # A
        initial_guess = [frequency_guess,
                         amplitude_guess, phase_guess, offset_guess]

        current_1_signal, current_1_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.current_1_data_points, p0=initial_guess)
        current_2_signal, current_2_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.current_2_data_points, p0=initial_guess)
        current_3_signal, current_3_covariance = curve_fit(
            f=self.sine_signal, xdata=self.timestamp_n, ydata=self.current_3_data_points, p0=initial_guess)

        return current_1_signal, current_2_signal, current_3_signal

    def get_signal_attributes(self, signal):
        frequency_fit, amplitude_fit, phase_fit, offset_fit = signal
        return frequency_fit, amplitude_fit, phase_fit, offset_fit

    def get_rms_value(self, data_points: list) -> float | None:
        if not data_points:
            return None

        squared_measurements = [measurement **
                                2 for measurement in data_points]
        mean = sum(squared_measurements) / len(squared_measurements)
        rms_value = np.sqrt(mean)
        return rms_value


class Powers(ModelSignals):
    def get_active_power(self) -> float:
        active_power = 0
        for measurement in self.last_measurements:
            active_power += measurement.voltage_1 * measurement.current_1
            active_power += measurement.voltage_2 * measurement.current_2
            active_power += measurement.voltage_3 * measurement.current_3
        return active_power

    def get_apparent_power(self, signal):
        voltage_1_signal, voltage_2_signal, voltage_3_signal = self.get_voltage_signals()
        current_1_signal, current_2_signal, current_3_signal = self.get_current_signals()
        signal
        squared_signal = np.square(signal)
        mean_squared_signal = np.mean(squared_signal)
        rms = np.sqrt(mean_squared_signal)

    def get_reactive_power(self):
        # TODO Q =sqrt(S**2-P**2)
        pass

    def get_power_factor(self):
        # TODO PF = P/S
        pass
