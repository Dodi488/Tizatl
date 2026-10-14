import sys
import select

# For Unix-based systems (Linux / macOS)
try:
    import tty
    import termios
    IS_WINDOWS = False
except ImportError:
    # Fallback for Windows
    import msvcrt
    IS_WINDOWS = True


def get_key_unix():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        
        # If the key starts with ESC (\x1b), capture following bytes in the sequence
        if ch == '\x1b':
            seq = ch
            # Read any additional queued characters (e.g. '[A' for Up Arrow)
            while True:
                r, _, _ = select.select([sys.stdin], [], [], 0.02)
                if r:
                    seq += sys.stdin.read(1)
                else:
                    break
            return seq
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_key_windows():
    ch = msvcrt.getch()
    # Windows special keys send \x00 or \xe0 followed by a scan code
    if ch in (b'\x00', b'\xe0'):
        return ch + msvcrt.getch()
    return ch.decode('latin-1')


def main():
    print("Press any key to inspect its ANSI code / raw representation.")
    print("Press Ctrl+C to exit.\n")

    while True:
        try:
            key = get_key_windows() if IS_WINDOWS else get_key_unix()

            # Ctrl+C check
            if key in ('\x03', b'\x03'):
                print("\r\nExiting...")
                break

            # Raw string representation (\x1b[A)
            repr_str = repr(key)
            
            # Printable escape string (e.g., \e[A or \x1b[A)
            esc_str = key.replace('\x1b', '\\e')
            
            # Hex values
            hex_str = ' '.join(f"\\x{ord(c):02x}" for c in key)

            print(f"\rKey Pressed: {repr_str:<15} | Escape: {esc_str:<12} | Hex: {hex_str}\r")

        except KeyboardInterrupt:
            print("\r\nExiting...")
            break


if __name__ == "__main__":
    main()
