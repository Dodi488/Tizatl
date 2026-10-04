#import os
import sys
#from dataclasses import dataclass, field, astuple, replace
#import termios
#import atexit
#import errno

sys.dont_write_bytecode = True

from terminal import enable_raw_mode, get_window_size
from input import editor_process_keypress
from output import editor_refresh_screen
from data import E

def init_editor() -> None:
    E.cx = 0
    E.cy = 0

    try:
        get_window_size(E)
    except OSError:
        die("get_window_error")

def main():
    enable_raw_mode()
    init_editor()

    while True:
        editor_refresh_screen()
        editor_process_keypress()

if __name__ == "__main__":
    main()
