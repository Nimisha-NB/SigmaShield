import subprocess
import time
import atexit
import signal
import sys
from setproxy import set_mac_proxy, reset_mac_proxy

mitm_process = None

def start():
    set_mac_proxy("Wi-Fi", "127.0.0.1", 8080)  # Start the Proxy
    time.sleep(1)
    global mitm_process
    mitm_process = start_mitm_proxy()  # Start the MITM Proxy
    # Start the AI Models here

def start_mitm_proxy(script_path="./setproxy.py"):
    try:
        process = subprocess.Popen(
            ["mitmdump", "-s", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ mitmdump started successfully.")
        return process
    except FileNotFoundError:
        print("❌ mitmdump not found. Is it installed and in your PATH?")
    except Exception as e:
        print(f"❌ Failed to start mitmdump: {e}")

def cleanup():
    print("👋 Bye")
    if mitm_process:
        mitm_process.terminate()
        print("🛑 mitmdump terminated.")
    reset_mac_proxy("Wi-Fi")  # Replace with your service name

# Register cleanup function
atexit.register(cleanup)

# Handle keyboard interrupt (Ctrl+C) and other signals
def handle_signal(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

# Main
if __name__ == "__main__":
    start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
