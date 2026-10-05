import sys
from dataclasses import dataclass, field
from typing import Any

from data import realloc

sys.dont_write_bytecode = True

@dataclass
class Abuf:
    b: bytearray = field(default_factory=bytearray) # This is not necessary because in Python strings are dynamic or we could use an numpy array (np.zeros).
    length: int = 0

def ab_append(ab: Abuf, s: str, length: int) -> Any:
    new = realloc(ab.b, ab.length + length)

    if (new == None): return
    new[ab.length : ab.length + length] = s.encode("utf-8")
    ab.b = new
    ab.length += length

def ab_free(ab: Abuf) -> Any:
    ab.b = bytearray()
