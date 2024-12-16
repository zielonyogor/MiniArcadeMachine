import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene
import time

SQUARE_SIZE = 64

class MinesweeperScene(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)
        # left, right, up, right
        self.squares = [fig.Square(8, 100, SQUARE_SIZE, '#FFFF00'),
                        fig.Square(160, 100, SQUARE_SIZE, '#0000FF')]
    
    def enter(self):
        pass

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

        for i in range(len(self.squares)):
            self.display.blit(self.squares[i].surf, self.squares[i])
        

        pygame.display.update()
