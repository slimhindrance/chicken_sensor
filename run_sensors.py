import subprocess
import time
import os
import sys

# List of scripts to run (replace with actual paths to your scripts)
scripts = [
    '/home/cwl21/audio_logger_least.py',
    '/home/cwl21/audio_logger_mid.py',
    '/home/cwl21/audio_logger_most.py',
    '/home/cwl21/motion_logger_green.py',
    '/home/cwl21/motion_logger_yellow.py',
    '/home/cwl21/motion_logger_purple.py',
    '/home/cwl21/light_logger.py'
]

def run_script(script_name):
    """Run a given script in a new subprocess."""
    try:
        process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error running script {script_name}: {e}")
        return None

def main():
    processes = []

    # Start all scripts
    for script in scripts:
        print(f"Starting {script}...")
        process = run_script(script)
        if process:
            processes.append(process)
        else:
            print(f"Failed to start {script}")

    # Monitor all scripts and restart if any fail
    try:
        while True:
            for i, process in enumerate(processes):
                # Check if the process is still running
                retcode = process.poll()
                if retcode is not None:  # Process has ended
                    print(f"Script {scripts[i]} has stopped with exit code {retcode}. Restarting...")
                    # Restart the script
                    new_process = run_script(scripts[i])
                    processes[i] = new_process  # Replace old process with new one

            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Main script interrupted. Stopping all processes.")
        for process in processes:
            process.terminate()  # Gracefully terminate all scripts
        for process in processes:
            process.wait()  # Wait for each process to finish
        print("All processes have been terminated.")

if __name__ == '__main__':
    main()
