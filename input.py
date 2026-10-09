import sys
import os

sys.dont_write_bytecode = True

from terminal import editor_read_key
from data import CTRL_KEY, STDOUT_FILENO, E, EditorKey, Erow, QUIT_TIMES
from editor_operations import editor_insert_char, editor_del_char, editor_insert_char, editor_insert_new_line
from file_io import editor_save
from output import editor_set_status_message, editor_refresh_screen

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
        if c == b'\r':
            editor_insert_new_line()
            return

        if c[0] == CTRL_KEY('q'):
            if E.dirty and E.quit_times > 0:
                editor_set_status_message(f"WARNING!!! File has unsaved changes. Press Ctrl-Q {E.quit_times} more times to quit.")
                E.quit_times -= 1
                return

            os.write(STDOUT_FILENO, b'\x1b[2J'[:4])
            os.write(STDOUT_FILENO, b'\x1b[H'[:3])
            sys.exit(0)

        if c[0] == CTRL_KEY('s'):
            editor_save()
            return

        if c == EditorKey.HOME_KEY.value:
            E.cx = 0
            return

        if c == EditorKey.END_KEY.value:
            if E.cy < E.numrows:
                E.cx = E.row[E.cy].size
            return

        if c == EditorKey.BACKSPACE.value or c[0] == CTRL_KEY('h') or c == EditorKey.DEL_KEY.value:
            if c == EditorKey.DEL_KEY.value: editor_move_cursor(EditorKey.MOVE_RIGHT.value)
            editor_del_char()
            return

        if c == EditorKey.PAGE_UP.value or c == EditorKey.PAGE_DOWN.value:
            if c == EditorKey.PAGE_UP.value:
                E.cy = E.rowoff
            elif c == EditorKey.PAGE_DOWN.value:
                E.cy = E.rowoff + E.screenrows - 1
                if E.cy > E.numrows: E.cy = E.numrows

            times = E.screenrows
            while times != 0:
                editor_move_cursor(EditorKey.MOVE_UP.value if c == EditorKey.PAGE_UP.value else EditorKey.MOVE_DOWN.value)
                times -= 1
            return

        if c in EditorKey:
            editor_move_cursor(c)
        elif c[0] == CTRL_KEY('l') or c == '\x1b':
            return
        else:
            editor_insert_char(c)

        E.quit_times = QUIT_TIMES
