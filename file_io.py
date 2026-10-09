import sys
import errno

from data import E, Erow
from terminal import die
from row_operations import editor_insert_row
from output import editor_set_status_message

sys.dont_write_bytecode = True

def editor_rows_to_string(blufen: int) -> str: # "".joind(blufen)?
    totlen = 0
    for j in range(E.numrows):
        totlen += E.row[j].size + 1
    buflen = totlen

#    buf = bytearray(totlen)
#    n = 0
#    p = buf[n]
#    for j in range(E.numrows):
#        p = (E.row[j].chars)[E.row[j].size]
#        p += E.row[j].size
        # p = p + '\n'
#        n += 1

    buf = [""] * totlen # bytearray(buflen)
    for j in range(E.numrows):
        buf[j] = E.row[j].chars + '\n'

    return ''.join(buf)

def editor_open(filename: str) -> None:
    E.filename = filename

    try:
        with open(filename, "r") as f:
            #line = f.readline()
            #line = f.read()
            for line in f:
                linelen = len(line)
                while linelen > 0 and (line[linelen - 1] == '\n' or line[linelen - 1] == '\r'): linelen -= 1
                editor_insert_row(E.numrows, line[:linelen], linelen)
                E.dirty = False

    except OSError:
        die("open")

    #linelen = len(line)    
    #linelen = 1
    #while linelen > 0 and (line[linelen - 1] == '\n' or line[linelen - 1] == '\r'): linelen -= 1

    #E.row.size = linelen
    #E.row.chars = [b'0'] * (linelen + 1)
    #E.row.chars[:linelen] = line
    #E.row.chars[linelen] = '\0' This is not necessary in python.
    #E.row.chars = ''.join(E.row.chars[:-1]) # There is a bug, the last character is b'0' so join fails (because all other characters are strings).
    #E.numrows -= 1
    #editor_append_row(line, linelen)

    # free(line) and fclose(fp)

def editor_save() -> None:
    from input import editor_prompt
    if E.filename == "":
        E.filename = editor_prompt("Save as: {} (ESC to cancel)")
        if E.filename == "":
            editor_set_status_message("Save aborted")
            return

    length = 0
    buf = editor_rows_to_string(length)
    length = len(buf.encode("utf-8"))

    try:
        with open(E.filename, "w") as f:
            f.write(buf)
            E.dirty = False
            editor_set_status_message(f"{length} bytes written to disk")
    except OSError as e:
        editor_set_status_message(f"Can't save! I/O error: {e.errno}")
