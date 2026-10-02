#import os
import sys
#from dataclasses import dataclass, field, astuple, replace
#import termios
#import atexit
#import errno

sys.dont_write_bytecode = True

from terminal import enable_raw_mode
from input import editor_process_keypress
from output import editor_refresh_screen

def main():
    enable_raw_mode()

    while True:
        editor_refresh_screen()
        editor_process_keypress()

if __name__ == "__main__":
    main()
