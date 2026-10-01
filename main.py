import os
import sys

def main():
    STDIN_FILENO = sys.stdin.fileno()

    while True:
        c = os.read(STDIN_FILENO, 1)
        if not c or c == b'q':
            break

if __name__ == "__main__":
    main()
