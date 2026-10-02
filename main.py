import os
import sys
from dataclasses import dataclass, field, astuple
import termios

STDIN_FILENO = sys.stdin.fileno()

@dataclass
class Raw:
    iflag: int
    oflag: int
    cflag: int
    lflag: int
    ispeed: int
    ospeed: int
    cc: list[str | int] = field(default_factory=list) 

def enable_raw_mode() -> None:
    variables = termios.tcgetattr(STDIN_FILENO)
    raw = Raw(*variables)
    raw.lflag = raw.lflag & ~ termios.ECHO
    raw = list(astuple(raw))
    termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, raw)
    # The proble with this code is that Python does not actually set values with pointers like c does, we are just creating a local copy and modifying it.
    # We are going to define a class and alter its values.

def main():
    enable_raw_mode()
    while True:
        c = os.read(STDIN_FILENO, 1)
        if not c or c == b'q':
            break

if __name__ == "__main__":
    main()
