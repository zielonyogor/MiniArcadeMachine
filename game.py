import pygame
from pygame.locals import *

from game_scene import GameStatemanager
from select_scene import SelectScene
from match2_scene import Match2
from simonsays_scene import SimonSays
from minesweeper_scene import MinesweeperScene
from leaderboard import LeaderboardScene

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320

FPS = 10

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
        self.font = pygame.font.SysFont('arial', 24)
        self.clock = pygame.time.Clock()
        
        self.game_state_manager = GameStatemanager('select')
        self.game_state_manager.setup(self)

        self.is_running = True
        self.scenes = {'select': SelectScene(self.screen, self.game_state_manager, self.font),
                       'match2': Match2(self.screen, self.game_state_manager, self.font),
                       'simonsays': SimonSays(self.screen, self.game_state_manager, self.font),
                       'minesweeper': MinesweeperScene(self.screen, self.game_state_manager, self.font),
                       'leaderboard': LeaderboardScene(self.screen, self.game_state_manager, self.font)}
    
    def run(self):
        while self.is_running:
            current_state = self.game_state_manager.get_state()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.is_running = False
                    elif event.key == K_x and self.game_state_manager.get_state() != 'select':
                        self.game_state_manager.change_state('select')
                    else:
                        self.scenes[current_state].update(event)
                elif event.type == QUIT:
                    self.is_running = False
                else:
                    self.scenes[current_state].update(event)
            
            self.scenes[current_state].run()
            pygame.display.update()
            
            self.clock.tick(FPS)
