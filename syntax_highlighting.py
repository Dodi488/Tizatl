import sys

from data import Erow, realloc
from defines import EditorHighlight

sys.dont_write_bytecode = True

def is_separator(c: str) -> bool:
    return c.isspace() or c == '\0' or c in ",.()+-/*=~%<>[];"

def editor_update_syntax(row: Erow) -> None:
    # row.hl = realloc(row.hl, row.rize) This is not correct because row.hl is a string and realloc is for bytearray (choose one!).
    #row.hl = EditorHighlight.HL_NORMAL.value
    # We have to actually use a variant of memset because now its a list, not a string.
    #row.hl = row.hl * row.size
    #row.hl = list(row.hl)
    row.hl[:] = [EditorHighlight.HL_NORMAL.value] * row.rsize

    prev_state = 1

    #for i in range(row.rsize):
    #    if row.render[i].isdigit():
    #        row.hl[i] = EditorHighlight.HL_NUMBER.value

    i = 0
    while i < row.rsize:
        c = row.render[i]
        prev_hl = row.hl[i - 1] if i > 0 else EditorHighlight.HL_NORMAL.value

        if (c.isdigit() and (prev_state or prev_hl == EditorHighlight.HL_NUMBER.value) or (c == '.' and prev_hl == EditorHighlight.HL_NUMBER.value)):
            row.hl[i] = EditorHighlight.HL_NUMBER.value
            i += 1
            prev_state = 0
            continue

        prev_state = is_separator(c)
        i += 1

def editor_syntax_to_color(hl: int) -> int:
    match hl:
        case EditorHighlight.HL_NUMBER.value:
            return 31
        case EditorHighlight.HL_MATCH.value:
            return 34
        case _:
            return 37
