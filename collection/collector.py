#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import os

GPIO.setmode(GPIO.BOARD)

# define the pin that goes to the circuit
pin_to_circuit = 7

# Define the directory to save files
save_directory = os.path.expanduser("~/Desktop/lake")

# Ensure the directory exists
os.makedirs(save_directory, exist_ok=True)


def rc_time(pin_to_circuit):
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(pin_to_circuit) == GPIO.LOW:
        count += 1

    return count


def get_next_5_minute_mark():
    """Calculate the next 5-minute mark from the current time."""
    now = datetime.now()
    next_mark = (now + timedelta(minutes=5)).replace(second=0, microsecond=0)
    next_mark = next_mark - timedelta(minutes=now.minute % 5)
    return next_mark


# Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    readings = []  # List to store readings
    next_save_time = get_next_5_minute_mark()

    while True:
        # Get the current reading
        reading = rc_time(pin_to_circuit)
        readings.append(reading)  # Collect the reading
        print(reading)

        # Check if it's time to save the readings
        if datetime.now() >= next_save_time:
            # Generate a timestamped filename
            timestamp = next_save_time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_directory, f"readings_{timestamp}.txt")

            # Save all readings to the file
            with open(filename, "w") as file:
                file.write("\n".join(map(str, readings)))

            print(f"Saved readings to {filename}")

            # Reset the readings list and calculate the next save time
            readings = []
            next_save_time += timedelta(minutes=5)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
