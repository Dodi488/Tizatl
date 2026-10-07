import sys
from dataclasses import fields

from data import E, realloc, Erow, TAB_STOP_SIZE

sys.dont_write_bytecode = True

def editor_row_cx_to_rx(row: Erow, cx: int) -> int:
    rx = 0
    for j in range(cx):
        if row.chars[j] == '\t':
            rx += (TAB_STOP_SIZE - 1) - (rx % TAB_STOP_SIZE)
        rx += 1

    return rx

def editor_update_row(row: Erow) -> None:
    tabs = 0
    for j in range(row.size):
        if row.chars[j] == '\t': tabs += 1

    row.render = "0" * (row.size + tabs * (TAB_STOP_SIZE - 1) + 1)

    idx = 0
    row.render = list(row.render)
    for j in range(row.size):
        if row.chars[j] == '\t':
            row.render[idx] = " "
            idx += 1
            while (idx % TAB_STOP_SIZE != 0):
                row.render[idx] = " "
                idx += 1
        else:
            row.render[idx] = row.chars[j]
            idx += 1

    #row.render[idx:] = '\0' # This is not necessary in python.
    row.render = "".join(row.render[:idx])
    row.rsize = idx

def editor_append_row(s: str, linelen: int) -> None:
    at = E.numrows
    E.row.append(Erow(size=linelen, chars=s, rsize=0, render=""))

    editor_update_row(E.row[at])

    E.numrows += 1
    E.dirty = True

def editor_row_insert_char(row: Erow, at: int, c: int) -> None:
    if at < 0 or at > row.size: at = row.size 

    row.chars = row.chars[:at] + c.decode("utf-8") + row.chars[at:]
    row.size += 1

    editor_update_row(row)
    E.dirty = True
