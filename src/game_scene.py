import pygame
from pygame.locals import *

class Scene:
    def __init__(self, display, game_state_manager, font) -> None:
        self.display = display
        self.game_state_manager = game_state_manager
        self.font = font
    #for reseting
    def enter(self):
        pass
    def update(self, input):
        pass
    def run(self):
        pass

class GameStatemanager:
    def __init__(self, current_state) -> None:
        self.current_state = current_state
        self.game = None
    def setup(self, game):
        self.game = game
    def get_state(self):
        return self.current_state
    def change_state(self, new_state):
        self.current_state = new_state
        self.game.scenes[self.current_state].enter()
    def enter_name_scene(self, game, score):
        self.current_state = 'entername'
        self.game.scenes[self.current_state].enter(game, score)
    def turn_off(self):
        self.game.is_running = False