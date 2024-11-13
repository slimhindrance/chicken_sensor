import time
import smbus
import sys

I2C_BUS = 1
SENSOR_ADDR = 0x23

bus = smbus.SMBus(I2C_BUS)

# Command constants for the BH1750 sensor
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_H_MODE = 0x10

def initialize_sensor():
    """Initializes the light sensor."""
    try:
        # Power on the sensor
        bus.write_byte(SENSOR_ADDR, POWER_ON)
        time.sleep(0.1)
        
        # Reset the sensor
        bus.write_byte(SENSOR_ADDR, RESET)
        time.sleep(0.1)

        # Set the sensor to continuous high-resolution mode
        bus.write_byte(SENSOR_ADDR, CONTINUOUS_H_MODE)
        print("Sensor initialized successfully.")
    
    except IOError as e:
        print(f"Error initializing the sensor: {e}")
        sys.exit(1)

def read_light_level():
    """Reads light level data from the sensor."""
    try:
        # Read 2 bytes of data from the sensor
        data = bus.read_i2c_block_data(SENSOR_ADDR, CONTINUOUS_H_MODE, 2)
        
        # Combine the two bytes into a 16-bit integer value
        light_level = (data[0] << 8) + data[1]
        return light_level
    except IOError as e:
        print(f"Error reading data from the sensor: {e}")
        return None

def log_light_data():
    """Logs the light data to a file and prints to the console."""
    try:
        with open("/home/cwl21/light_log.txt", "a") as log_file:
            while True:
                # Read the light level
                light_level = read_light_level()

                if light_level is not None:
                    # Format the log entry with timestamp
                    log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Light Level: {light_level} lux"
                    
                    # Write the log entry to the file and print to console
                    log_file.write(log_entry + '\n')
                    print(log_entry)
                
                # Wait 1 second before logging the next entry
                time.sleep(1)
    except KeyboardInterrupt:
        print("Logging stopped by user.")
    except IOError as e:
        print(f"Error writing to the log file: {e}")
    finally:
        print("Exiting the program.")

if __name__ == "__main__":
    # Initialize the sensor and start logging
    initialize_sensor()
    log_light_data()
