import os
import sys
from dataclasses import dataclass, field, astuple, replace
import termios
import atexit

# Helper functions
# This one can be replace by importing urses.ascii.iscntrl()
def iscntrl(char):
    char = char.decode("utf-8") # In c we dont have to do this convertion.
    if isinstance(char, str):
        val = int(ord(char)) 
    else:
        val = char
    return (0 <= val <= 31) or (val == 127)

@dataclass
class TtyAttributes:
    iflag: int
    oflag: int
    cflag: int
    lflag: int
    ispeed: int
    ospeed: int
    cc: list[str | int] = field(default_factory=list)

STDIN_FILENO = sys.stdin.fileno()

orig_termios = TtyAttributes(*termios.tcgetattr(STDIN_FILENO))

def disable_raw_mode(tty_attributes: TtyAttributes) -> None:
    global orig_termios
    termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(orig_termios)))

def enable_raw_mode() -> None:
    global orig_termios
    atexit.register(disable_raw_mode, orig_termios)

    raw = replace(orig_termios)
    raw.iflag &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
    raw.oflag &= ~(termios.OPOST)
    raw.cflag &= ~(termios.CS8)
    raw.lflag &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    raw = list(astuple(raw))
    termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, raw)
    # The proble with this code is that Python does not actually set values with pointers like c does, we are just creating a local copy and modifying it.
    # We are going to define a class and alter its values.

def main():
    enable_raw_mode()
    while (c := os.read(STDIN_FILENO, 1)) and c != b'q':
        if iscntrl(c):
            print(f"c[0]\r")
        else:
            print(f"{ord(c)} ('{c.decode("utf-8")}')\r")

if __name__ == "__main__":
    main()
