import time
from gpiozero import Button

# Set up GPIO pin 27 as a button input (with internal pull-down resistor)
button = Button(27, pull_up=False)  # pull_up=False means it's using the internal pull-down resistor

def log_state_change(state):
    # Record the time and the state change
    state_str = 'HIGH' if state else 'LOW'
    log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, GPIO 26 State: {state_str}\n"
    
    with open("gpio27_live_log.txt", "a") as log_file:
        log_file.write(log_entry)
    
    print(log_entry)  # Optionally print to the console

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
