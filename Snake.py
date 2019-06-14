from ConsoleGames.ConsoleGraphic import Console
from ConsoleGames.Stuff import Timer
from keyboard import is_pressed
from random import randint

WEIRD_CHARS = {'BLOCK': chr(9608),
               'WEIRD BLOCK': chr(9688),
               'SPACE sx': chr(9594), 'SPACE dx': chr(9592),
               'DIAMOND sx': chr(9668), 'DIAMOND dx': chr(9658)}


class Snake:
    textures = {None: ' ', ' ': ' ',
                '|': '|', '-': '-', '+': '+',
                '0': WEIRD_CHARS['BLOCK'],
                'O': WEIRD_CHARS['WEIRD BLOCK'],
                ')': WEIRD_CHARS['SPACE dx'], '(': WEIRD_CHARS['SPACE sx'],
                '>': WEIRD_CHARS['DIAMOND dx'], '<': WEIRD_CHARS['DIAMOND sx'],
                '@': '@', '[': '[', ']': ']'
                }

    def __init__(self, width: int, height: int, pac_man: bool=False, time_per_move=0.4):
        self.width = width
        self.height = height
        self.pac_man = pac_man
        self.game_area = [[None for _ in range(width)] for __ in range(height)]
        self.head_position = [
                              height//2,  # Y
                              width//2    # X
                             ]
        self.game_area[self.head_position[0]][self.head_position[1]] = 1
        self.game_area[self.head_position[0]][self.head_position[1]-1] = 2
        self.length = 2
        self.direction = 'R'
        self.place_food()
        self.timer = Timer(time_per_move)
        self.console = Console((width+1)*2, height+2, Snake.textures)
        self.console.griglia = self.render_frame()

    def place_food(self):
        food_pos = [randint(0, self.height-1), randint(0, self.width-1)]
        if self.game_area[food_pos[0]][food_pos[1]] is not None:
            self.place_food()
            return
        self.game_area[food_pos[0]][food_pos[1]] = '@'

    def fail(self):
        print(self.length)
        input()
        raise SystemExit

    def wim(self):  # what (happens) if (it) moves?
        new_pos = self.head_position.copy()
        if self.direction == 'R':
            new_pos[1] += 1
        elif self.direction == 'U':
            new_pos[0] -= 1
        elif self.direction == 'L':
            new_pos[1] -= 1
        elif self.direction == 'D':
            new_pos[0] += 1

        if (not 0 <= new_pos[0] < self.height) or (not 0 <= new_pos[1] < self.width):
            if self.pac_man:
                new_pos[0] = new_pos[0] % self.height
                new_pos[1] = new_pos[1] % self.width
            else:
                self.fail()
        t = self.game_area[new_pos[0]][new_pos[1]]
        if isinstance(t, int) and t != self.length:
            self.fail()

        if self.game_area[new_pos[0]][new_pos[1]] == '@':
            self.place_food()
            self.length += 1
        return new_pos

    def move(self):
        def above_max(x): return None if x+1 > self.length else x+1
        self.head_position = self.wim().copy()
        self.game_area = [[above_max(x) if isinstance(x, int) else x for x in row] for row in self.game_area]
        self.game_area[self.head_position[0]][self.head_position[1]] = 1

    def render_frame(self):
        res = []
        for row in self.game_area:
            new_row = []
            for cell in row:
                temp = ''  # maybe unneeded ?
                if cell is None:
                    temp = '()'
                elif cell == 1:
                    temp = '00'
                elif cell == self.length:
                    temp = '<0'
                elif isinstance(cell, int):
                    temp = 'OO'
                elif cell == '@':
                    temp = '[]'
                else:
                    temp = [None, None]
                new_row.append(temp[0])
                new_row.append(temp[1])
            res.append(new_row)
        res = [['+', '+'] * self.width] + res + [['+', '+'] * self.width]
        res = [['+'] + row + ['+'] for row in res]
        return res

    def exe(self):
        self.console.refresh_un()
        self.timer.reset()
        while True:
            if self.timer.elapsed():
                self.timer.reset()
                self.move()
                self.console.refresh(self.render_frame())
            if is_pressed('RIGHT'):
                self.direction = 'R'
            if is_pressed('UP'):
                self.direction = 'U'
            if is_pressed('LEFT'):
                self.direction = 'L'
            if is_pressed('DOWN'):
                self.direction = 'D'

    __call__ = exe


def test():
    f = Snake(10, 10)
    f.exe()
    input()
    while True:
        f.move()
        f.exe()
        input()


if __name__ == '__main__':
    Snake(
        int(input('size x(int): ')),
        int(input('size y(int): ')),
        input('PacMan effect([y]es/[n]o(n_yes))? ').lower() in ('yes', 'y'),
        float(input('time per move(float): '))
        )()
