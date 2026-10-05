import sys

from data import E, Erow
from terminal import die
from row_operations import editor_append_row

sys.dont_write_bytecode = True

def editor_open(filename: str) -> None:
    try:
        with open(filename, "r") as f:
            #line = f.readline()
            #line = f.read()
            for line in f:
                linelen = len(line)
                while linelen > 0 and (line[linelen - 1] == '\n' or line[linelen - 1] == '\r'): linelen -= 1
                editor_append_row(line, linelen)

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
