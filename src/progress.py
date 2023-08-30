import time, os

class ProgressBar:
    def __init__(self, title: str = 'Progress'):
        self.CODE_SAVE_CURSOR = '\x1b[s'
        self.CODE_RESTORE_CURSOR = '\x1b[u'
        self.CODE_CURSOR_IN_SCROLL_AREA = '\x1b[1A'
        self.COLOR_FG = '\x1b[30m'
        self.COLOR_BG = '\x1b[42m'
        self.COLOR_BG_BLOCKED = '\x1b[43m'
        self.RESTORE_BG = '\x1b[49m'
        
        self.PROGRESS_BLOCKED = False
        self.percentage = 0
        self.text_lines = []
        self.title = title
        
        _, self.lines = os.get_terminal_size()

        print('\x1b[2J', end='')
        print('\n', end='')
        print(self.CODE_SAVE_CURSOR, end='')
        print('\x1b[0;' + str(self.lines) + 'r', end='')
        print(self.CODE_RESTORE_CURSOR)
        print(self.CODE_CURSOR_IN_SCROLL_AREA, end='')

        self.draw(0)
    
    def print(self, line):
        self.text_lines.append(line)
        self.draw(self.percentage)
    
    def draw(self, percentage: int):
        if self.PROGRESS_BLOCKED:
            self.PROGRESS_BLOCKED = False

        _, self.lines = os.get_terminal_size()
        self.percentage = percentage

        print(self.CODE_SAVE_CURSOR, end='')
        print('\x1b[0;0f', end='')

        print('\r', flush=True, end='')
        
        self.__print_text_lines(self.text_lines[-self.lines - 2:])  
        print(self.CODE_RESTORE_CURSOR, end='')
        
        self.__print_progress_bar(percentage)  

    def halt(self):
        _, self.lines = os.get_terminal_size()
        self.PROGRESS_BLOCKED = True
        print(self.CODE_SAVE_CURSOR, end='')
        print('\x1b[0;0f', end='')

        print('\r', flush=True, end='')
        
        self.__print_text_lines(self.text_lines[-self.lines-2:])
        print(self.CODE_RESTORE_CURSOR, end='')
        
        print('\x1b[2J', flush=True, end='')
        self.__print_progress_bar(self.percentage + 1)
        print('\x1b[H', flush=True, end='')

    def destroy(self):
        print('\x1b[2J', end='')
        self.is_destroyed = True

    def __print_text_lines(self, lines):
        for i, line in enumerate(lines, start=1):
            print(f'\x1b[{i};0f{line}\x1b[K')
            if i >= self.lines - 2:
                break

    def __print_progress_bar(self, percentage: int):
        cols, _ = os.get_terminal_size()
        bar_size = cols - 17

        complete_size = (bar_size * percentage) / 100
        remainder_size = bar_size - complete_size

        if self.PROGRESS_BLOCKED:
            progress_bar = f'[{self.COLOR_BG_BLOCKED}{"#" * int(complete_size)}{self.RESTORE_BG}{"." * int(remainder_size)}]'
        else:
            progress_bar = f'[{self.COLOR_BG}{"#" * int(complete_size)}{self.RESTORE_BG}{"." * int(remainder_size)}]'
        print(f'\x1b[{self.lines - 1};0f{self.title} {percentage}% {progress_bar}\x1b[K', end='')

if __name__ == '__main__':
    pb = ProgressBar('Download')
    
    for i in range(101):
        if i == 50:
            pb.halt()
            input('Enter something: ')
        pb.draw(i)
        pb.print(str(i)+'abcdedsdfsdfsdfsdf')
        time.sleep(0.1)
    
    pb.destroy()
