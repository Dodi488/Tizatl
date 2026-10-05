#import os
import sys
#from dataclasses import dataclass, field, astuple, replace
#import termios
#import atexit
#import errno

sys.dont_write_bytecode = True

from terminal import enable_raw_mode, get_window_size, die
from input import editor_process_keypress
from output import editor_refresh_screen
from data import E
from file_io import editor_open

def init_editor() -> None:
    E.cx = 0
    E.cy = 0
    E.numrows = 0
    #E.row = None
    #E.row = ""
    #E.row = bytearray()
    E.row = []

    try:
        get_window_size(E)
    except OSError:
        die("get_window_error")

def main():
    enable_raw_mode()
    init_editor()
    if len(sys.argv) >= 2:
        editor_open(sys.argv[1])

    while True:
        editor_refresh_screen()
        editor_process_keypress()

if __name__ == "__main__":
    main()
