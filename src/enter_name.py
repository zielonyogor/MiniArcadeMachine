import pygame
from pygame.locals import *
from game_scene import Scene

import database as db
import math
import input

import buzzer
import threading

LETTERS = 8
    
class EnterNameScene(Scene):
    def __init__(self, display, game_state_manager, font):
        super().__init__(display, game_state_manager, font)
        
        self.prompt = self.font.render('ENTER YOUR NAME', False, (255, 255, 255))
        self.pointer = self.font.render('^', False, (255, 255, 255))

        self.letters = []
        self.letters_code = []

        self.was_updated = True
    
    def enter(self, game, score):
        self.letters = []
        self.letters_code = []
        for i in range(LETTERS):
            tex = self.font.render('_', False, (255, 255, 255))
            self.letters.append(tex)
            self.letters_code.append(91)
        
        self.game = game
        self.score = math.floor(score * 10) / 10
        
        self.current_index = 0
        
    def update(self):
        if input.get_button_input() == input.SELECT:
            print(self.letters_code, ' ', self.game, ' ', self.score)
            for i in range(len(self.letters_code)):
                if self.letters_code[i] == 91:
                    self.letters_code[i] = 95
            match self.game:
                case 'match_2':
                    db.add_match_2_score((''.join(chr(l) for l in self.letters_code), self.score))
                case 'simon_says':
                    db.add_simon_says_score((''.join(chr(l) for l in self.letters_code), self.score))
                case 'minesweeper':
                    db.add_minesweeper_score((''.join(chr(l) for l in self.letters_code), self.score))
            
            music_thread = threading.Thread(target=buzzer.play_happy_melody, daemon=True)
            music_thread.start()
            self.game_state_manager.change_state('select')
            return
        
        joystick = input.get_joystick_input()
        if joystick == input.NONE:
            return
        
        music_thread = threading.Thread(target=buzzer.play_select_melody, daemon=True)
        music_thread.start()
        if joystick == input.LEFT:
            self.current_index = (self.current_index - 1) % LETTERS
            self.was_updated = True
        elif joystick == input.RIGHT:
            self.current_index = (self.current_index + 1) % LETTERS
            self.was_updated = True
        elif joystick == input.UP:
            self.update_letter(-1)
        elif joystick == input.DOWN:
            self.update_letter(1)

            self.was_updated = True
    def run(self):
        # self.update_screen()
        if self.was_updated == True:
            self.update_screen()

    def update_screen(self):
        self.display.fill(pygame.Color('black'))
        
        self.display.blit(self.prompt, (20, 20))

        # change 19 to 18 if this offset looks off
        self.display.blit(self.pointer, (30 + 19 * self.current_index, 140))
        
        for i in range(LETTERS):
            self.display.blit(self.letters[i], (30 + 18*i, 120))

        pygame.display.update()
        self.was_updated = False
    
    def update_letter(self, value):
        self.letters_code[self.current_index] = (self.letters_code[self.current_index] + value - 65) % 27 + 65
        if self.letters_code[self.current_index] == 91:
            self.letters[self.current_index] = self.font.render('_', False, (255, 255, 255))
        else:
            self.letters[self.current_index] = self.font.render(str(chr(self.letters_code[self.current_index])), False, (255, 255, 255))
        self.was_updated = True

