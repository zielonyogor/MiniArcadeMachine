import pygame
from pygame.locals import *
from random import shuffle

import figures as fig
from globals import *
from game_scene import Scene
import time

SHOW_ALL_TIME = 3
SHOW_TIME = 0.8

SQUARE_SIZE = 36

class Match2(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)

        self.time_text = self.font.render('Time: 0000', False, (255, 255, 255))

        colors = ["#66CCFF", "#FF9966", "#FF0000", "#FF99FF", 
                        "#00CCCC", "#000099", "#CCFFFF", "#FFFF99"] #, "#66FF66", "#006600", "#330066", "#660066"
        self.colors = colors + colors
        
        shuffle(self.colors)
        self.available_colors = [self.colors[i * COLUMNS:(i + 1) * COLUMNS] for i in range(ROWS)]
        
        self.pointer = fig.Pointer()
    
    def enter(self):
        self.remaining = 8
        # Create a ROWS x COLUMNS matrix

        shuffle(self.colors)
        self.available_colors = [self.colors[i * COLUMNS:(i + 1) * COLUMNS] for i in range(ROWS)]

        self.squares = []
        self.placeholder = fig.Square(0, 0, SQUARE_SIZE, '#757575')
        self.squares_state = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)] # 0 - nothing, 1 - selected, 2 - taken
        self.selected = None

        for i in range(ROWS):
            y = i * (SQUARE_SIZE + 12) + 36
            l = []
            for j in range(COLUMNS):
                x = j * (SQUARE_SIZE + 12) + 16
                square = fig.Square(x, y, SQUARE_SIZE, self.available_colors[i][j])
                l.append(square)
            self.squares.append(l)

        self.state_time = time.time()
        self.start_time = 0
        self.current_time = 0

        self.squares_state = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)] # 0 - nothing, 1 - selected, 2 - taken
        self.state = 'show_all' # show-all - show all squares at the start
                                # game - basic game
                                # show - show two selected squares

        self.selected = None

    def update(self, input):
        if self.state != 'game':
            return
        if input.type != KEYDOWN:
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
            current_row = self.pointer.current_index[0]
            current_col = self.pointer.current_index[1]
            if(self.squares_state[current_row][current_col] == 0):
                self.squares_state[current_row][current_col] = 1
                
                if(self.selected != None):

                    current_color = self.available_colors[current_row][current_col]

                    prev_square_color = self.available_colors[self.selected[0]][self.selected[1]]
                    if(current_color == prev_square_color):
                        self.squares_state[current_row][current_col] = 2
                        self.squares_state[self.selected[0]][self.selected[1]] = 2
                        self.remaining -= 1
                    else:
                        self.squares_state[current_row][current_col] = 0
                        self.squares_state[self.selected[0]][self.selected[1]] = 0

                    self.state_time = time.time()
                    self.state = 'show'
                else:
                    self.selected = (current_row, current_col)
                    
            elif(self.squares_state[current_row][current_col] == 1):
                print('unselecting')
                self.selected = None
                self.squares_state[current_row][current_col] = 0
    def run(self):
        match self.state:
            case 'show_all':
                self.update_show_all()
            case 'game':
                self.update_game()
            case 'show':
                self.update_show()
            case _:
                pass
    
    def update_show_all(self):
        if time.time() - self.state_time > SHOW_ALL_TIME:
            self.state = 'game'
            self.start_time = time.time()
            return
        
        self.display.fill(pygame.Color('black'))
    
        for i in range(ROWS):
            for j in range(COLUMNS):
                self.display.blit(self.squares[i][j].surf, self.squares[i][j])
        pygame.display.update()
    
    def update_game(self):
        self.display.fill(pygame.Color('black'))

        for i in range(ROWS):
            y = i * (SQUARE_SIZE + 12) + 36
            for j in range(COLUMNS):
                x = j * (SQUARE_SIZE + 12) + 16
                if(self.squares_state[i][j] == 0):
                    self.display.blit(self.placeholder.surf, (x, y))
                elif(self.squares_state[i][j] == 1):
                    self.display.blit(self.squares[i][j].surf, self.squares[i][j])

        self.update_time()
        self.display.blit(self.time_text, (60, 2))
        
        pygame.draw.rect(self.display, pygame.Color('white'), self.pointer.rect, 4)

        pygame.display.update()

    def update_show(self):
        if time.time() - self.state_time > SHOW_TIME:
            self.selected = None
            
            # TODO: switch to leaderboard here instead of going to 
            if self.remaining == 0:
                self.game_state_manager.change_state('select')
                return
            
            self.state = 'game'
            return
        
        self.display.fill(pygame.Color('black'))

        for i in range(ROWS):
            y = i * (SQUARE_SIZE + 12) + 36
            for j in range(COLUMNS):
                x = j * (SQUARE_SIZE + 12) + 16
                if ((i, j) == self.selected) or ([i, j] == self.pointer.current_index):
                    self.display.blit(self.squares[i][j].surf, self.squares[i][j])
                elif (self.squares_state[i][j] == 0):
                    self.display.blit(self.placeholder.surf, (x, y))
        
        self.update_time()
        self.display.blit(self.time_text, (60, 2))

        pygame.display.update()

    def update_time(self):
        self.current_time = time.time() - self.start_time

        temp_string = f'{self.current_time:.1f}'.zfill(6)
        self.time_text = self.font.render(f'Time: {temp_string}', False, (255, 255, 255))