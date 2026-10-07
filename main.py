#import os
import sys
#from dataclasses import dataclass, field, astuple, replace
#import termios
#import atexit
#import errno

sys.dont_write_bytecode = True

from terminal import enable_raw_mode, get_window_size, die
from input import editor_process_keypress
from output import editor_refresh_screen, editor_set_status_message
from data import E
from file_io import editor_open

def init_editor() -> None:
    # We should probably define E here.
    # We could not only not define defaults in our dataclasses and this would make sense.
    # Python does not allow to initialize a datalclass and not put values (unless we have defaults or make the attributes optional).
    #E.cx = 0
    #E.cy = 0
    #E.rx = 0
    #E.rowoff = 0
    #E.coloff = 0
    #E.numrows = 0
    #E.row = []
    #E.filename = "New"
    #E.statusmsg[0] = '\0' # Cant add something to a string using slicing, either change statusmsg to an array or concatenate '\0' to the beggining.
    # E.statusmsg_time = 0

    try:
        get_window_size(E)
    except OSError:
        die("get_window_error")

    E.screenrows -= 2

def main():
    enable_raw_mode()
    init_editor()
    if len(sys.argv) >= 2:
        editor_open(sys.argv[1])

    editor_set_status_message("HELP: Ctrl-S = save | Ctrl-Q = quit")

    while True:
        editor_refresh_screen()
        editor_process_keypress()

if __name__ == "__main__":
    main()
