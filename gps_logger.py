import time
import serial
import gps

# Set up the serial connection
SERIAL_PORT = '/dev/serial0'  # Use /dev/serial0 on the Pi for UART
BAUD_RATE = 9600  # Baud rate (common for GPS modules)
gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

def initialize_serial():
    # Open the serial connection to the GPS module
    gps_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    return gps_serial

def read_gps_data(gps_serial):
    # Read the GPS data stream from the serial port
    while True:
        line = gps_serial.readline().decode('ascii', errors='replace').strip()
        if line:
            return line

def log_gps_data():
    with open("gps_log.txt", "a") as log_file:
        gps_serial = initialize_serial()
        
        while True:
            gps_data = read_gps_data(gps_serial)
            
            # Parse NMEA data (if using a GPS that outputs NMEA sentences)
            log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, GPS Data: {gps_data}\n"
            
            # Write to file
            log_file.write(log_entry)
            print(log_entry)  # Optionally print to console
            
            time.sleep(1)  # Adjust the sleep time to log data at your desired rate

if __name__ == "__main__":
    log_gps_data()
