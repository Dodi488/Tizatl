import sys
from dataclasses import fields

from data import E, realloc, Erow

sys.dont_write_bytecode = True

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

    #at = E.numrows
    #E.row[at].size = linelen
    #E.row[at].chars = [b'0'] * (linelen + 1)
    #E.row[at].chars[:linelen] = s
    #E.row[at].chars[linelen] = '\0'
    E.row.append(Erow(size=linelen, chars=s))
    E.numrows += 1
