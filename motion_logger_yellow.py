import time
from gpiozero import Button

pin = 16

# Set up GPIO pin  as a button input (with internal pull-down resistor)
button = Button(pin, pull_up=False)  # pull_up=False means it's using the internal pull-down resistor

def log_state_change(state):
    # Record the time and the state change (1 for pressed, 0 for released)
    state_value = 1 if state else 0
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    log_entry = f"({state_value}, '{timestamp}')\n"
    
    # Open the file in append mode and write the log entry
    with open(f"test_gpio{pin}_log.txt", "a") as log_file:
        log_file.write(log_entry)
    
    # Optionally print to the console
    print(log_entry)

def main():
    # Set up event listeners for button presses and releases
    button.when_pressed = lambda: log_state_change(True)
    button.when_released = lambda: log_state_change(False)

    try:
        # Keep the program running so it can detect state changes
        print("Logging state changes. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Sleep briefly to avoid using excessive CPU
    except KeyboardInterrupt:
        print("Logging stopped by user.")

if __name__ == "__main__":
    main()
