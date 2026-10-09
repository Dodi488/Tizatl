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

#def editor_append_row(s: str, linelen: int) -> None:
def editor_insert_row(at: int, s: str, length: int) -> None:
    if at < 0 or at > E.numrows: return

    #new_row = E.row.append(Erow(size=length, chars=s[:length], rsize=0, render=""))
    #E.row.insert(at, new_row)
    new_row = Erow(size=length, chars=s[:length], rsize=0, render="")
    E.row.insert(at, new_row)
    editor_update_row(E.row[at])

    E.numrows += 1
    E.dirty = True

def editor_free_row(row: Erow) -> None: # This is not necessary in python.
    row.render = ""
    row.chars = ""

def editor_del_row(at: int) -> None:
    if at < 0 or at >= E.numrows: return
    #editor_free_row(E.row[at])
    del E.row[at]
    #E.row[at] = E.row[at + 1]
    E.numrows -= 1
    E.dirty = True

def editor_row_insert_char(row: Erow, at: int, c: int) -> None:
    if at < 0 or at > row.size: at = row.size 
    row.chars = row.chars[:at] + c.decode("utf-8") + row.chars[at:]
    row.size += 1
    editor_update_row(row)
    E.dirty = True

def editor_row_append_string(row: Erow, s: str, length: int) -> None:
    #row.chars = row.chars + (" " * row.size + length + 1) This is not necessary because stings in python are dynamic.
    #row.chars[row.size] = s
    row.chars = row.chars[:row.size] + s + row.chars[row.size:]
    row.size += length
    #row.chars[row.size] = '\0' This is the same as row.chars = row.chars + '\0'
    editor_update_row(row)
    E.dirty = True

def editor_row_del_char(row: Erow, at: int) -> None:
    if at < 0 or at >= row.size: return
    row.chars = row.chars[:at] + row.chars[at + 1:]
    row.size -= 1
    editor_update_row(row)
    E.dirty = True
