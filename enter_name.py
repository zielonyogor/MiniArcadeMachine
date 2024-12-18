import pygame
from pygame.locals import *
from game_scene import Scene

import database as db

LETTERS = 12
    
class EnterNameScene(Scene):
    def __init__(self, display, game_state_manager, font):
        super().__init__(display, game_state_manager, font)
        
        self.prompt = self.font.render('ENTER YOUR NAME', False, (255, 255, 255))
        
        self.letters = []
        self.letters_code = []

        self.current_index = 0

        self.was_updated = True
    
    def enter(self):
        self.letters = []
        self.letters_code = []
        for i in range(LETTERS):
            tex = self.font.render('A', False, (255, 255, 255))
            self.letters.append(tex)
            self.letters_code.append(65)
        

    def update(self, input):
        if input.type == KEYDOWN:
            if input.key == K_LEFT:
                self.current_index = (self.current_index - 1) % LETTERS
                self.was_updated = True
            elif input.key == K_RIGHT:
                self.current_index = (self.current_index + 1) % LETTERS
                self.was_updated = True
            elif input.key == K_UP:
                self.update_letter(-1)
            elif input.key == K_DOWN:
                self.update_letter(1)

            self.was_updated = True
    def run(self):
        # self.update_screen()
        if self.was_updated == True:
            self.update_screen()

    def update_screen(self):
        self.display.fill(pygame.Color('black'))
        
        self.display.blit(self.prompt, (26, 20))
        
        for i in range(LETTERS):
            self.display.blit(self.letters[i], (14 + 18*i, 80))

        pygame.display.update()
        self.was_updated = False
    
    def update_letter(self, value):
        self.letters_code[self.current_index] = (self.letters_code[self.current_index] + value - 65) % 27 + 65
        if self.letters_code[self.current_index] == 91:
            self.letters[self.current_index] = self.font.render('_', False, (255, 255, 255))
        else:
            self.letters[self.current_index] = self.font.render(str(chr(self.letters_code[self.current_index])), False, (255, 255, 255))
        self.was_updated = True
