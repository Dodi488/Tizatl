import os
import sys

from data import STDOUT_FILENO, E

sys.dont_write_bytecode = True

def editor_draw_rows() -> None:
    for y in range(E.screenrows):
        os.write(STDOUT_FILENO, b'~\r\n'[:3])

def editor_refresh_screen() -> None:
    os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
    os.write(STDOUT_FILENO, b'\x1b[H'[:3])

    editor_draw_rows()

    os.write(STDOUT_FILENO, b'\x1b[H'[:3])
