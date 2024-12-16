import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene

class SelectScene(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)
        self.levels = [fig.Square(0, 0, ICON_SIZE, '#de90ad'), 
                        fig.Square(0, 0, ICON_SIZE, '#fcba03'), 
                        fig.Square(0, 0, ICON_SIZE, '#81d66f')]
        
        self.texts = [self.font.render('MATCH-2', False, (255, 255, 255)),
                      self.font.render('SIMONSAYS', False, (255, 255, 255)),
                      self.font.render('MINESWEEPER', False, (255, 255, 255))]

        self.current_index = 1
        self.was_updated = True
    def update(self, input):
        if input.type == KEYDOWN:
            if input.key == K_LEFT:
                self.current_index = (self.current_index - 1) % 3
            elif input.key == K_RIGHT:
                self.current_index = (self.current_index + 1) % 3
            elif input.key == K_z:
                match self.current_index:
                    case 0:
                        self.game_state_manager.change_state('match2')
                        print('match2')
                    case 1:
                        self.game_state_manager.change_state('simonsays')
                        print('simonsays')
                    case 2:
                        self.game_state_manager.change_state('minesweeper')
                        print('minesweeper')
                        
            self.was_updated = True
    def run(self):
        self.display.fill(pygame.Color('black'))
        
        self.display.blit(self.levels[(self.current_index - 1 + 3) % 3].surf, (10, 100))
        
        self.display.blit(self.texts[self.current_index], (60, 70))
        self.display.blit(self.levels[self.current_index].surf, (90, 100))
        
        self.display.blit(self.levels[(self.current_index + 1) % 3].surf, (170, 100))

        pygame.display.update()
        self.was_updated = False
