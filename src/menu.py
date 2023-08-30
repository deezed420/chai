import sys

class Menu:
    def __init__(self, title: str, options: list) -> str:
        self.title = title
        self.options = options
        self.selected_index = 0
    
    def display(self, selector: str = '>', exit: bool = False):
        if exit: self.options.append('Exit')
        self.selector = selector

        print('\x1b[2J')

        while True:
            self.__display_menu()
            key = self.__getkey()

            if key == 'up' and self.selected_index > 0: self.selected_index -= 1
            elif key == 'down' and self.selected_index < len(self.options) - 1: self.selected_index += 1
            elif key == 'select': return self.options[self.selected_index]

    def __getch(self):
        if sys.platform == 'linux':
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
        elif sys.platform == 'win32':
            from msvcrt import getch
            return getch()

    def __getkey(self):
        firstChar = self.__getch()
        try:
            if sys.platform == 'linux':
                if firstChar == '\x1b':
                    return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[self.__getch() + self.__getch()]
                elif firstChar == chr(3):
                    raise KeyboardInterrupt
                elif firstChar in [chr(10), chr(13)]:
                    return 'select'
                else:
                    return firstChar
            else:
                if firstChar == b'\xe0':
                    return {'H': 'up', 'P': 'down', 'M': 'right', 'K': 'left'}[self.__getch().decode()]
                elif firstChar == b'\x03':
                    raise KeyboardInterrupt
                elif firstChar == b'\r':
                    return 'select'
                else:
                    return firstChar
        except KeyError: pass
            
    def __display_menu(self):
        sys.stdout.write('\033[H')
        sys.stdout.flush()

        print(self.title)

        for idx, option in enumerate(self.options):
            if idx == self.selected_index:
                print(f"{self.selector} {option}")
            else:
                print(f"  {option}")

if __name__ == '__main__':
    menu = print(Menu('Main Menu', ['Option 1', 'Option 2', 'Option 3']).display())