import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene
import time
import random
import database as db


SQUARE_SIZE = 18
ROWS = 9
COLUMNS = 9

class MinesweeperScene(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)

        self.time_text = self.font.render('Time: 0000', False, (255, 255, 255))
        
        self.pointer = fig.Pointer(SQUARE_SIZE, ROWS, COLUMNS, 24, 36, 4)
        self.square_icon = fig.Square(0, 0, SQUARE_SIZE, '#CCCCCC')

        
        self.number_font = pygame.font.SysFont('arial', 20, bold=True)
        self.text_numbers = []

        texts_and_colors = [
            ('B', (255, 0, 0)),
            ('1', (0, 0, 255)),
            ('2', (0, 255, 0)),
            ('3', (255, 0, 0)),
            ('4', (94, 23, 176)),
            ('5', (140, 10, 55)),
            ('6', (10, 191, 158)),
            ('7', (0, 0, 0)),
            ('8', (137, 138, 102))
        ]

        for text, color in texts_and_colors:
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            rendered_text = self.number_font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            surface.blit(rendered_text, text_rect)
            self.text_numbers.append(surface)
        
        self.placeholder = fig.Square(0, 0, SQUARE_SIZE, '#757575')
    
    def enter(self):
        self.bombs = self.randomize_bombs()
        self.find_numbers()
        self.squares_state = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)] # 0 - hidden, 1 - shown

        self.current_time = 0
        self.start_time = time.time()
        self.found = 0

        self.is_over = False
        self.won = False

    def update(self, input):
        if input.type != KEYDOWN:
            return
        
        if self.is_over:
            if input.key == K_z:
                if not self.won:
                    self.game_state_manager.change_state('select')
                    return
                if db.is_better_minesweeper(self.current_time):
                    self.game_state_manager.enter_name_scene('minesweeper', f'{self.current_time:.1f}')
                else:
                    self.game_state_manager.change_state('select')
            return
        
        if input.key == K_LEFT:
            self.pointer.move(-1, 0)
        elif input.key == K_RIGHT:
            self.pointer.move(1, 0)
        elif input.key == K_UP:
            self.pointer.move(0, -1)
        elif input.key == K_DOWN:
            self.pointer.move(0, 1)
        elif input.key == K_z:
            row = self.pointer.current_index[0]
            column = self.pointer.current_index[1]
            if self.squares_state[row][column] == 1:
                return
            if self.square_numbers[row][column] == -1:
                print('Game Over')
                self.show_end()
                return
            if self.square_numbers[row][column] == 0:
                self.reveal_connected_zeros(row, column)
            else:
                self.squares_state[row][column] = 1
                self.found += 1
            if self.found == ROWS * COLUMNS - 10:
                print('Wygrana')
                self.won = True
                self.show_end()

    def run(self):
        if self.is_over:
            return
        
        self.display.fill(pygame.Color('black'))

        for i in range(ROWS):
            for j in range(COLUMNS):
                y = i * (SQUARE_SIZE + 4) + 36
                x = j * (SQUARE_SIZE + 4) + 24
                if self.squares_state[i][j] == 1:
                    self.display.blit(self.square_icon.surf,  (x, y))
                    if self.square_numbers[i][j] > 0:
                        self.display.blit(self.text_numbers[self.square_numbers[i][j]], (x, y))
                else:
                    self.display.blit(self.placeholder.surf, (x, y))

        pygame.draw.rect(self.display, pygame.Color('white'), self.pointer.rect, 4)

        self.update_time()
        self.display.blit(self.time_text, (60, 2))

        pygame.display.update()
    
    def update_time(self):
        self.current_time = time.time() - self.start_time

        temp_string = f'{self.current_time:.1f}'.zfill(6)
        self.time_text = self.font.render(f'Time: {temp_string}', False, (255, 255, 255))

    def show_end(self):
        self.is_over = True

        self.display.fill(pygame.Color('black'))

        for i in range(ROWS):
            for j in range(COLUMNS):
                y = i * (SQUARE_SIZE + 4) + 36
                x = j * (SQUARE_SIZE + 4) + 24
                self.display.blit(self.square_icon.surf,  (x, y))
                if self.square_numbers[i][j] > 0:
                    self.display.blit(self.text_numbers[self.square_numbers[i][j]], (x, y))
                elif self.square_numbers[i][j] == -1:
                    self.display.blit(self.text_numbers[0], (x, y))

        self.display.blit(self.time_text, (60, 2))

        pygame.display.update()

    # algorithm related methods
    def randomize_bombs(self):
        bombs = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        for i in range(10):
            number = random.randrange(0, ROWS*COLUMNS)
            while number in bombs:
                number = random.randrange(0, ROWS*COLUMNS)
            print(number)
            bombs[i] = number
        return bombs

    def find_numbers(self):
        self.square_numbers = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        for b in self.bombs:
            y = b // ROWS
            x = b % COLUMNS
            self.square_numbers[y][x] = -1

        def is_valid(row, col):
            return 0 <= row < ROWS and 0 <= col < COLUMNS

        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
            (0, -1),         (0, 1),     # left,        right
            (1, -1), (1, 0), (1, 1)      # bottom-left, bottom, bottom-right
        ]
        
        # Count bombs around each cell
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.square_numbers[row][col] == -1:
                    continue 
                bomb_count = 0
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if is_valid(new_row, new_col) and self.square_numbers[new_row][new_col] == -1:
                        bomb_count += 1
                self.square_numbers[row][col] = bomb_count
        print(self.square_numbers)
    
    def reveal_connected_zeros(self, row, column):
        def is_valid(row, col):
            return 0 <= row < ROWS and 0 <= col < COLUMNS and self.squares_state[row][col] == 0

        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
            (0, -1),         (0, 1),     # left,        right
            (1, -1), (1, 0), (1, 1)      # bottom-left, bottom, bottom-right
        ]

        stack = [(row, column)]

        while stack:
            cur_row, cur_col = stack.pop()
            if not is_valid(cur_row, cur_col):
                continue

            # Reveal the current square
            self.squares_state[cur_row][cur_col] = 1
            self.found += 1

            # If the square is 0, add its neighbors to the stack
            if self.square_numbers[cur_row][cur_col] == 0:
                for dr, dc in directions:
                    new_row, new_col = cur_row + dr, cur_col + dc
                    if is_valid(new_row, new_col):
                        stack.append((new_row, new_col))