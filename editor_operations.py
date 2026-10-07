import sys

sys.dont_write_bytecode = True

from data import E, Erow
from row_operations import editor_append_row, editor_row_insert_char, editor_row_del_char

def editor_insert_char(c: int) -> None:
    if E.cy == E.numrows:
        editor_append_row("", 0)

    editor_row_insert_char(E.row[E.cy], E.cx, c)
    E.cx += 1

def editor_del_char() -> None:
    if E.cy == E.numrows: return

    #row = Erow(E.row[E.cy])
    if E.cx > 0:
        editor_row_del_char(E.row[E.cy], E.cx - 1)
        E.cx -= 1
