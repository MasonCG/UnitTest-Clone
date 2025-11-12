import os

def clear_terminal():
    """Clears the terminal screen based on the operating system."""

    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (POSIX systems)
    else:
        for i in range(5):
            _ = os.system('clear')
