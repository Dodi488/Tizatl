import os
import sys
#from dataclasses import dataclass
import termios

STDIN_FILENO = sys.stdin.fileno()

def enable_raw_mode() -> None:
    raw = termios.tcgetattr(STDIN_FILENO)
    raw["lflag"] = raw["lflag"] & ~ termios.ECHO
    raw = termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH)
    # The proble with this code is that Python does not actually set values with pointers like c does, we are just creating a local copy and modifying it.
    # We are going to define a class and alter its values.

def main():
    while True:
        c = os.read(STDIN_FILENO, 1)
        if not c or c == b'q':
            break

if __name__ == "__main__":
    main()
