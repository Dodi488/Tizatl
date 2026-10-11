import sys

from data import Erow, realloc
from defines import EditorHighlight

sys.dont_write_bytecode = True

def editor_update_syntax(row: Erow) -> None:
    # row.hl = realloc(row.hl, row.rize) This is not correct because row.hl is a string and realloc is for bytearray (choose one!).
    #row.hl = EditorHighlight.HL_NORMAL.value
    # We have to actually use a variant of memset because now its a list, not a string.
    #row.hl = row.hl * row.size
    #row.hl = list(row.hl)
    row.hl[:] = [EditorHighlight.HL_NORMAL.value] * row.rsize

    for i in range(row.rsize):
        if row.render[i].isdigit():
            row.hl[i] = EditorHighlight.HL_NUMBER.value

def editor_syntax_to_color(hl: int) -> int:
    match hl:
        case EditorHighlight.HL_NUMBER.value:
            return 31
        case _:
            return 37
