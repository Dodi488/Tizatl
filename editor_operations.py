import sys

sys.dont_write_bytecode = True

from data import E
from row_operations import editor_append_row, editor_row_insert_char

def editor_insert_char(c: int) -> None:
    if E.cy == E.numrows:
        editor_append_row("", 0)

    editor_row_insert_char(E.row[E.cy], E.cx, c)
    E.cx += 1
