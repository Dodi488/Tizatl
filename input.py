import sys
import os

sys.dont_write_bytecode = True

from terminal import editor_read_key
from data import CTRL_KEY, STDOUT_FILENO, E, EditorKey, Erow

sys.dont_write_bytecode = True

def editor_move_cursor(key: bytes) -> None:
    row = None if E.cy >= E.numrows else E.row[E.cy]

    match key:
        case EditorKey.MOVE_LEFT.value:
            if E.cx != 0:
                E.cx -= 1
            elif E.cy > 0:
                E.cy -= 1
                E.cx = E.row[E.cy].size
        case EditorKey.MOVE_RIGHT.value:
            if (row and E.cx < row.size):
                E.cx += 1
            elif (row and E.cx == row.size):
                E.cy += 1
                E.cx = 0
        case EditorKey.MOVE_UP.value:
            if E.cy != 0:
                E.cy -= 1
        case EditorKey.MOVE_DOWN.value:
            if E.cy != E.numrows:
                E.cy += 1

    row = None if E.cy >= E.numrows else E.row[E.cy]
    rowlen = row.size if row else 0
    if E.cx > rowlen: E.cx = rowlen

def editor_process_keypress() -> None:
    c = editor_read_key()
    if c:
        if c[0] == CTRL_KEY('q'):
            os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
            os.write(STDOUT_FILENO, b'\x1b[H'[:3])
            sys.exit(0)

        if c == EditorKey.HOME_KEY.value:
            E.cx = 0

        if c == EditorKey.END_KEY.value:
            E.cx = E.screencols - 1

        if c == EditorKey.PAGE_UP.value or c == EditorKey.PAGE_DOWN.value:
            times = E.screenrows
            while times != 0:
                editor_move_cursor(EditorKey.MOVE_UP.value if c == EditorKey.PAGE_UP.value else EditorKey.MOVE_DOWN.value)
                times -= 1

        if c in EditorKey:
            editor_move_cursor(c)
