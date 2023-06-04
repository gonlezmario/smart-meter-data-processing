# Smart Meter Python Script
This repository contains a Python script for a smart meter application 
that runs as a service. The script connects to a configurable MQTT server
and displays relevant electrical data dynamically in a Matplotlib figure.

## Prerequisites
Before running the script, ensure that you have the following
prerequisites installed:

Python (version 3.6 or higher)
MQTT broker/server
Required Python packages -> listed in requirements.txt
(Optional) Test that the MQTT broker is correctly configured running
mock_data_generator.py

## Configuration
Open the config.py file in a text editor and modify the following parameters
according to your MQTT server:

### Database
url - By default local db -> sqlite:///database.db

### MQTT
broker_address - MQTT server address
port - MQTT communication port (Usually 8883)
topic - Topic listened to by this service

### Plotting
maximum_plot_points - controls the maximum numbers of points plotted at once
price_per_kwh - Used to calculate expected price, this value is usually dynamic

## Usage
Make sure the configuration is set properly and the MQTT service runs correctly.
Run main script afterwards. In case of error or unexpected behavior, there is
a log file available.

A figure should pop up, displaying in pseudo-real-time up to 3 phase voltages,
currents, active power, reactive power, apparent power, power factor, energy
consumption and expected price in €.

Note that if a database is not correctly set up, a default local "database.db" 
will automatically be created.

To stop the script, press Ctrl + C in the terminal or close the figure window.

## Contributing
Contributions to this project are welcome. If you encounter any issues or have
suggestions for improvements, please open an issue or submit a pull request.

## Disclaimer
This script is provided as-is, without any warranty or guarantee.
Use it at your own risk.
