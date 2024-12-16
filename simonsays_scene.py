import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene
import time

SQUARE_SIZE = 64

class SimonSays(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)
        # left, right, up, right
        self.squares = [fig.Square(8, 100, SQUARE_SIZE, '#FFFF00'),
                        fig.Square(160, 100, SQUARE_SIZE, '#0000FF'),
                        fig.Square(84, 60, SQUARE_SIZE, '#FF0000'),
                        fig.Square(84, 140, SQUARE_SIZE, '#00FF00')]
    
    def enter(self):
        self.score = 0

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
        
        self.update_score()

        pygame.display.update()

    def update_score(self):
        score_texture = self.font.render(f'Score: {f'{self.score}'.zfill(4)}', False, (255, 255, 255))
        self.display.blit(score_texture, (50, 2))