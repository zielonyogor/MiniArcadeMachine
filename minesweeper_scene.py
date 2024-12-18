import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene
import time


SQUARE_SIZE = 18
ROWS = 9
COLUMNS = 9

class MinesweeperScene(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)

        self.time_text = self.font.render('Time: 0000', False, (255, 255, 255))
        
        self.squares = []

        for i in range(ROWS):
            y = i * (SQUARE_SIZE + 4) + 36
            l = []
            for j in range(COLUMNS):
                x = j * (SQUARE_SIZE + 4) + 24
                square = fig.Square(x, y, SQUARE_SIZE, '#FFFFFF')
                l.append(square)
            self.squares.append(l)
        
        self.start_time = 0
        self.current_time = 0
    
    def enter(self):
        self.start_time = time.time()
        self.current_time = 0

    def update(self, input):
        if input.type != KEYDOWN:
            return
        if input.key == K_LEFT:
            pass
        elif input.key == K_RIGHT:
            pass
        elif input.key == K_UP:
            pass
        elif input.key == K_DOWN:
            pass

    def run(self):
        self.display.fill(pygame.Color('black'))

        for i in range(ROWS):
            for j in range(COLUMNS):
                self.display.blit(self.squares[i][j].surf, self.squares[i][j])
        
        self.update_time()
        self.display.blit(self.time_text, (50, 2))

        pygame.display.update()
    
    def update_time(self):
        self.current_time = time.time() - self.start_time

        temp_string = f'{self.current_time:.1f}'.zfill(6)
        self.time_text = self.font.render(f'Time: {temp_string}', False, (255, 255, 255))