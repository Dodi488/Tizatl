import sys
import os
from collections.abc import Callable

sys.dont_write_bytecode = True

from terminal import editor_read_key
from data import CTRL_KEY, STDOUT_FILENO, E, EditorKey, Erow, QUIT_TIMES, iscntrl
from editor_operations import editor_insert_char, editor_del_char, editor_insert_char, editor_insert_new_line
from file_io import editor_save
from output import editor_set_status_message, editor_refresh_screen
from find import editor_find

sys.dont_write_bytecode = True

def editor_prompt(prompt: str, callback: Callable[[str, bytes], None] | None = None) -> str:
    bufsize = 128
    #buf = bytearray(bufsize)
    #buf = [" "] * bufsize 
    #buf = E.filename
    buf = ""

    buflen = 0
    #buf[0] = b'\0'

    while True:
        message = prompt.format(buf)
        editor_set_status_message(message)
        editor_refresh_screen()

        c = editor_read_key()
        if c == EditorKey.DEL_KEY.value or c[0] == CTRL_KEY('h') or c == EditorKey.BACKSPACE.value:
            #if buflen != 0: buf[buflen - 1] = '\0'
            if buflen != 0:
                buf = buf[:-1]
                buflen -= 1
        elif c == b'\x1b':
            editor_set_status_message("")
            if callback: callback(buf, c)
            return None
        elif c == b'\r':
            if buflen != 0:
                editor_set_status_message("")
                if callback: callback(buf, c)
                return buf

        elif not iscntrl(c) and c[0] < 128:
            #if buflen == bufsize - 1:
                #bufsize *= 2
                #buf = realloc(buf, bufsize)
            buflen += 1
            #buf[buflen] = ord(c)
            #buf[buflen] = c.decode("utf-8")
            #print(buf)
            #0[0] = 0
            #buf[buflen] = '\0' # This is not necessary in python and I think it will cause an error.
            buf = buf + c.decode("utf-8")

        if callback: callback(buf, c)

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

        if c[0] == CTRL_KEY('f'):
            editor_find()
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
