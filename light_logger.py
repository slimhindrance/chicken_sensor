import time
import smbus

I2C_BUS = 1
SENSOR_ADDR = 0x23

bus = smbus.SMBus(I2C_BUS)

POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_H_MODE = 0x10

def initialize_sensor():
	bus.write_byte(SENSOR_ADDR, POWER_ON)
	time.sleep(0.1)
	
	bus.write_byte(SENSOR_ADDR, RESET)
	time.sleep(0.1)

	bus.write_byte(SENSOR_ADDR, CONTINUOUS_H_MODE)

def read_light_level():
	data = bus.read_i2c_block_data(SENSOR_ADDR, CONTINUOUS_H_MODE, 2)

	light_level = (data[0]<<8)+data[1]
	return light_level

def log_light_data():
	with open("light_log.txt", "a") as log_file:
		while True:
			light_level = read_light_level()
			log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, Light Level: {light_level} lux"
			
			log_file.write(log_entry)
			log_file.write('')
			print(log_entry)
			time.sleep(1)

if __name__ == "__main__":
	initialize_sensor()
	log_light_data()
