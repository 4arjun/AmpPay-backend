import serial
import requests

# Set up serial communication with the Arduino
ser = serial.Serial('/dev/tty.usbmodem1101', 9600)
  # Replace 'COMX' with the appropriate port for your Arduino
ser.timeout = 5  # Set a timeout for serial communication

# URL of your Django server's receive_data endpoint
Django_URL = 'http://localhost:8000/api/receive-data/'

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode().strip()  # Assuming each line from the Arduino is a complete data packet
        
        # Check if the received data starts with "Data:"
        if data.startswith("Data:"):
            # Remove the prefix and split the remaining data
            values = data[len("Data:"):].split(',')
            # Ensure the correct number of values are received
            if len(values) == 5:
                username, rms_current, rms_power, kilowatt_hours, peak_power = values
                # Prepare the payload for the HTTP POST request
                payload = {
                    'username': username,
                    'rms_current': float(rms_current),
                    'rms_power': float(rms_power),
                    'kilowatt_hours': float(kilowatt_hours),
                    'peak_power': float(peak_power)
                }
                # Send HTTP POST request to Django server
                response = requests.post(Django_URL, json=payload)
                if response.status_code == 200:
                    print("Data sent successfully to Django server")
                else:
                    print(f"Failed to send data to Django server. Response code: {response.status_code}")
            else:
                print("Invalid data format received")
        else:
            print("Invalid data received: Data prefix missing")
except KeyboardInterrupt:
    ser.close()  # Close serial connection when script is terminated