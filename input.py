import sys
import os

sys.dont_write_bytecode = True

from terminal import editor_read_key
from data import CTRL_KEY, STDOUT_FILENO

sys.dont_write_bytecode = True

def editor_process_keypress() -> None:
    c = editor_read_key()
    if c and c[0] == CTRL_KEY('q'):
        os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
        os.write(STDOUT_FILENO, b'\x1b[H'[:3])
        sys.exit(0)
