#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
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
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(pin_to_circuit) == GPIO.LOW:
        count += 1

    return count


# Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    start_time = time.time()
    readings = []  # List to store readings
    while True:
        # Get the current reading
        reading = rc_time(pin_to_circuit)
        readings.append(reading)  # Collect the reading
        print(reading)

        # Check if 5 minutes have passed
        if time.time() - start_time >= 300:  # 300 seconds = 5 minutes
            # Generate a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_directory, f"readings_{timestamp}.txt")

            # Save all readings to the file
            with open(filename, "w") as file:
                file.write("\n".join(map(str, readings)))

            print(f"Saved readings to {filename}")

            # Reset the timer and clear the readings list
            start_time = time.time()
            readings = []

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
