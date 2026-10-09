import sys

sys.dont_write_bytecode = True

from data import E, Erow
from row_operations import editor_insert_row, editor_row_insert_char, editor_row_del_char, editor_row_append_string, editor_del_row, editor_update_row

def editor_insert_char(c: int) -> None:
    if E.cy == E.numrows:
        editor_insert_row(E.numrows, "", 0)

    editor_row_insert_char(E.row[E.cy], E.cx, c)
    E.cx += 1

def editor_insert_new_line() -> None:
    if E.cx == 0:
        editor_insert_row(E.cy, "", 0)
    else:
        row = E.row[E.cy]
        tail = row.chars[E.cx:]
        editor_insert_row(E.cy + 1, tail, len(tail))
        row = E.row[E.cy]
        row.size = E.cx
        #row.chars[row.size] = '\0'
        row.chars = row.chars[:E.cx]
        editor_update_row(row)

    E.cy += 1
    E.cx = 0

def editor_del_char() -> None:
    if E.cy == E.numrows: return
    if E.cx == 0 and E.cy == 0: return

    row = E.row[E.cy]
    if E.cx > 0:
        editor_row_del_char(row, E.cx - 1)
        E.cx -= 1
    else:
        E.cx = E.row[E.cy - 1].size
        editor_row_append_string(E.row[E.cy - 1], row.chars, row.size)
        editor_del_row(E.cy)
        E.cy -= 1
