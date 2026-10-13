import sys
from dataclasses import fields

from data import EditorSyntax
from defines import HL_HIGHLIGHT_NUMBERS, HL_HIGHLIGHT_STRINGS

sys.dont_write_bytecode = True

C_HL_extensions = [".c", ".h", ".cpp"]
C_HL_keywords = ["switch", "if", "while", "for", "break", "continue", "return", "else",
  "struct", "union", "typedef", "static", "enum", "class", "case",
  "int|", "long|", "double|", "float|", "char|", "unsigned|", "signed|",
  "void|"]

HLDB = [EditorSyntax("c", HL_HIGHLIGHT_NUMBERS | HL_HIGHLIGHT_STRINGS, "//", "/*", "*/",  C_HL_extensions, C_HL_keywords)]

#HLDB_ENTRIES = len(HLDB) / len(HDLB[0])  # Is this really necessary in python? I think this is just plain wrong.
HLDB_ENTRIES = len(HLDB)
