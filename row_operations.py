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
    #E.row.size = linelen
    #E.row.chars = [b'0'] * (linelen + 1)
    #E.row.chars[:linelen] = line
    #E.row.chars[linelen] = '\0' This is not necessary in python.
    #E.row.chars = ''.join(E.row.chars[:-1]) # There is a bug, the last character is b'0' so join fails (because all other characters are strings).
    #E.numrows = 1

    #E.row = realloc(E.row, (len(fields(Erow)) * (E.numrows + 1)))
    #print(E.row)
    #E.row.resize(len(fields(Erow)) * (E.numrows + 1))
    #print(E.row)

    at = E.numrows
    #E.row[at].size = linelen
    #E.row[at].chars = [b'0'] * (linelen + 1)
    #E.row[at].chars[:linelen] = s
    #E.row[at].chars[linelen] = '\0'
    E.row.append(Erow(size=linelen, chars=s, rsize=0, render=""))

    #E.row[at].rsize = 0
    #E.row[at].render = ""
    editor_update_row(E.row[at])

    E.numrows += 1

def editor_row_insert_char(row: Erow, at: int, c: int) -> None:
    if at < 0 or at > row.size: at = row.size
    #row.chars = realloc(bytearray(row.chars, "utf-8"), row.size + 2)
    #row.chars[at + 1] = row.chars[at]
    #row.size += 1
    #row.chars[at] = c[0]
    #row.chars = row.chars.decode("utf-8")

    row.chars = row.chars[:at] + c.decode("utf-8") + row.chars[at:]
    row.size += 1

    editor_update_row(row)
