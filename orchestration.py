import subprocess
import time
import sys

# List of scripts to run (replace with actual paths to your scripts)
scripts = [
    '/home/pi/audio_logger_least.py',
    '/home/pi/audio_logger_mid.py',
    '/home/pi/audio_logger_most.py',
    '/home/pi/motion_logger_green.py',
    '/home/pi/motion_logger_yellow.py',
    '/home/pi/motion_logger_purple.py',
    '/home/pi/light_logger.py'
]

def run_script(script_name):
    """Run a given script in a new subprocess."""
    try:
        process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error running script {script_name}: {e}")
        return None

def start_http_server(directory='/home/pi/shared_files', port=8000):
    """Start a simple HTTP server in the specified directory."""
    try:
        process = subprocess.Popen(["python3", "-m", "http.server", str(port), "--directory", directory],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"HTTP server started on port {port} serving directory {directory}")
        return process
    except Exception as e:
        print(f"Error starting HTTP server: {e}")
        return None

def main():
    # Start the HTTP server
    http_server_process = start_http_server()

    # Start all other scripts
    processes = []
    for script in scripts:
        print(f"Starting {script}...")
        process = run_script(script)
        if process:
            processes.append(process)
        else:
            print(f"Failed to start {script}")

    # Monitor all scripts and restart if any stop unexpectedly
    try:
        while True:
            for i, process in enumerate(processes):
                retcode = process.poll()
                if retcode is not None:  # Process has ended
                    print(f"Script {scripts[i]} stopped with exit code {retcode}. Restarting...")
                    processes[i] = run_script(scripts[i])  # Restart the script
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Main script interrupted. Stopping all processes.")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()
        print("All processes have been terminated.")
        # Stop the HTTP server
        if http_server_process:
            http_server_process.terminate()
            http_server_process.wait()
            print("HTTP server terminated.")

if __name__ == '__main__':
    main()