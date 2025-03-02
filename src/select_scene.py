import pygame
from pygame.locals import *

import figures as fig
from globals import *
from game_scene import Scene
import input

import buzzer
import threading

class SelectScene(Scene):
    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)
        self.levels = [fig.Square(0, 0, ICON_SIZE, '#de90ad'), 
                        fig.Square(0, 0, ICON_SIZE, '#fcba03'), 
                        fig.Square(0, 0, ICON_SIZE, '#81d66f'),
                        fig.Square(0, 0, ICON_SIZE, '#123456'),
                        fig.Square(0, 0, ICON_SIZE, '#ba0041')]
        
        self.texts = [self.font.render('MATCH-2', False, (255, 255, 255)),
                      self.font.render('SIMONSAYS', False, (255, 255, 255)),
                      self.font.render('MINESWEEPER', False, (255, 255, 255)),
                      self.font.render('LEADERBOARD', False, (255, 255, 255)),
                      self.font.render('EXIT', False, (255, 255, 255))]

        self.current_index = 0
        self.was_updated = True
    def update(self):
        joystick = input.get_joystick_input()
        if joystick == input.LEFT:
            music_thread = threading.Thread(target=buzzer.play_select_melody, daemon=True)
            music_thread.start()
            self.current_index = (self.current_index - 1) % 5
        elif joystick == input.RIGHT:
            music_thread = threading.Thread(target=buzzer.play_select_melody, daemon=True)
            music_thread.start()
            self.current_index = (self.current_index + 1) % 5
            
        if input.get_button_input() == input.SELECT:
            match self.current_index:
                case 0:
                    self.game_state_manager.change_state('match2')
                case 1:
                    self.game_state_manager.change_state('simonsays')
                case 2:
                    self.game_state_manager.change_state('minesweeper')
                case 3:
                    self.game_state_manager.change_state('leaderboard')
                case 4:
                    self.game_state_manager.turn_off()
            return         
        self.was_updated = True
        
    def run(self):
        self.display.fill(pygame.Color('black'))
        
        self.display.blit(self.levels[(self.current_index - 1 + 5) % 5].surf, (10, 100))
        
        self.display.blit(self.texts[self.current_index], (120 - self.texts[self.current_index].get_width() // 2, 40))
        self.display.blit(self.levels[self.current_index].surf, (90, 100))
        
        self.display.blit(self.levels[(self.current_index + 1) % 5].surf, (170, 100))

        pygame.display.update()
        self.was_updated = False