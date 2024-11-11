import time
import board
import adafruit_dht

# Initialize the DHT sensor on GPIO4 (adjust if needed)
dht_device = adafruit_dht.DHT22(board.D4)

def log_sensor_data():
    with open("dht_log.txt", "a") as log_file:
        while True:
            try:
                # Read temperature and humidity from the DHT22 sensor
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                # Log the data with timestamp
                if temperature is not None and humidity is not None:
                    log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Temp: {temperature:.2f}°C, Humidity: {humidity:.2f}%\n"
                    log_file.write(log_entry)
                    print(log_entry)  # Print to the console as well
                else:
                    print("Failed to retrieve data from the sensor. Try again.")

            except Exception as e:
                print(f"Error reading sensor: {e}")

            # Sleep for 1 second before the next reading
            time.sleep(1)

if __name__ == "__main__":
    try:
        log_sensor_data()
    except KeyboardInterrupt:
        print("Logging stopped by user.")
