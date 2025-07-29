import time

def keep_alive():
    print("[SYS] Keep-alive loop running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[SYS] Shutdown signal received.")
