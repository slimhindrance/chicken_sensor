import time
from gpiozero import Button

# Set up GPIO pin 27 as a button input (with internal pull-down resistor)
button = Button(27, pull_up=False)  # pull_up=False means it's using the internal pull-down resistor

def log_gpio_state():
    with open("gpio27_log.txt", "a") as log_file:
        while True:
            # Check if the button is pressed (True) or not (False)
            gpio_state = button.is_pressed

            # Log the state with timestamp
            log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, GPIO 27 State: {'HIGH' if gpio_state else 'LOW'}\n"
            log_file.write(log_entry)
            print(log_entry)  # Optionally print to the console

            # Sleep for 1 second before reading again
            time.sleep(1)

if __name__ == "__main__":
    try:
        log_gpio_state()
    except KeyboardInterrupt:
        print("Logging stopped by user.")
