import os
import sys
from dataclasses import dataclass, field, astuple, replace
import termios
import atexit
import errno

#from data import TtyAttributes, STDIN_FILENO, perror, orig_termios
from data import *

sys.dont_write_bytecode = True

def die(s: str) -> None:
    os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
    os.write(STDOUT_FILENO, b'\x1b[H'[:3])

    perror(s)
    sys.exit(1)

#def disable_raw_mode(tty_attributes: TtyAttributes) -> None:
def disable_raw_mode() -> None:
    try:
        #termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(tty_attributes.orig_termios)))
        termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(E.orig_termios)))
    except termios.error:
        die("tcsetattr")

def enable_raw_mode() -> None:
    try:
        E.orig_termios = TtyAttributes(*termios.tcgetattr(STDIN_FILENO))
    except termios.error:
        die("tcgetattr")

    #atexit.register(disable_raw_mode, orig_termios)
    atexit.register(disable_raw_mode)

    raw = replace(E.orig_termios)
    raw.iflag &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
    raw.oflag &= ~(termios.OPOST)
    raw.cflag |= (termios.CS8)
    raw.lflag &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    raw.cc[termios.VMIN] = 0
    raw.cc[termios.VTIME] = 1

    try:
        termios.tcsetattr(STDIN_FILENO, termios.TCSAFLUSH, list(astuple(raw)))
    except termios.error:
        die("tcsetattr")
    # The proble with this code is that Python does not actually set values with pointers like c does, we are just creating a local copy and modifying it.
    # We are going to define a class and alter its values.

def editor_read_key() -> bytes:
    while True:
        try:
            c = os.read(STDIN_FILENO, 1)
            if c:
                return c
        except OSError as e:
            if e.errno != errno.EAGAIN:
                die("read")
