import os
import time

def child_process_function():
    """Function executed by the child process."""
    print("Child process: Starting its work...")
    time.sleep(3)  # Simulate some work
    print("Child process: Finishing its work and exiting.")
    os._exit(0)  # Exit the child process gracefully

if __name__ == "__main__":
    print("Main process: Starting.")

    pid = os.fork()

    if pid == 0:  # This is the child process
        child_process_function()
    else:  # This is the parent (main) process
        print(f"Main process: Forked a child process with PID {pid}.")
        print("Main process: Continuing its own tasks...")
        time.sleep(2)  # Simulate some work in the main process
        print("Main process: Done with its immediate tasks.")
        time.sleep(2)
        # The main process can now continue, while the child process runs in the background.
        # If the main process needs to wait for the child, it can use os.waitpid(pid, 0)
        # If the main process needs to kill the child, it can use os.kill(pid, signal.SIGTERM)
        # For this example, we simply let the main process continue and the child exit on its own.
        print("Main process: Exiting.")