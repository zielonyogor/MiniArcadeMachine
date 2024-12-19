import pygame
from pygame.locals import *
from game_scene import Scene

import database as db

ICON_SIZE = 64

class Place():
    def __init__(self, x, y, font, data = [0, '.......................', '000']):
        self.font = font
        self.text_nr = font.render(str(data[0]), False, (255, 255, 255))
        self.text_name = font.render(data[1], False, (255, 255, 255))
        self.text_score = font.render(str(data[2]), False, (255, 255, 255))
        self.dest = (x, y)
    
    def change_text(self, new_data):
        self.text_nr = self.font.render(str(new_data[0]), False, (255, 255, 255))
        self.text_name = self.font.render(new_data[1], False, (255, 255, 255))
        self.text_score = self.font.render(str(new_data[2]), False, (255, 255, 255))
    
class LeaderboardScene(Scene):
    def __init__(self, display, game_state_manager, font):
        super().__init__(display, game_state_manager, font)
        
        self.texts = [self.font.render('MATCH-2', False, (255, 255, 255)),
                      self.font.render('SIMONSAYS', False, (255, 255, 255)),
                      self.font.render('MINESWEEPER', False, (255, 255, 255))]
        
        self.match_leaderboards = []
        self.simonsays_leaderboards = []
        self.minesweeper_leaderboards = []

        for i in range(6):
            match_score = Place(10, 40 + 20 * i, font)
            self.match_leaderboards.append(match_score)

            simon_says = Place(10, 40 + 20 * i, font)
            self.simonsays_leaderboards.append(simon_says)
            
            minesweeper_score = Place(10, 40 + 20 * i, font)
            self.minesweeper_leaderboards.append(minesweeper_score)

        self.current_index = 1

        db.init()
    
    def enter(self):    
        self.current_index = 1
    
        match2_scores = db.get_match_2_scores()
        simonsays_scores = db.get_simon_says_scores()
        minesweeper_scores = db.get_minesweeper_scores()
        for i in range(len(match2_scores)):
            self.match_leaderboards[i].change_text(match2_scores[i])
        for i in range(len(simonsays_scores)):
            self.simonsays_leaderboards[i].change_text(simonsays_scores[i])
        for i in range(len(minesweeper_scores)):
            self.minesweeper_leaderboards[i].change_text(minesweeper_scores[i])
        self.was_updated = True

    def update(self, input):
        if input.type == KEYDOWN:
            if input.key == K_LEFT:
                self.current_index = (self.current_index - 1) % 3
                self.was_updated = True
            elif input.key == K_RIGHT:
                self.current_index = (self.current_index + 1) % 3
                self.was_updated = True

            self.was_updated = True
    def run(self):
        # self.update_screen()
        if self.was_updated == True:
            self.was_updated = False
            self.update_screen()

    def update_screen(self):
        self.display.fill(pygame.Color('black'))
        
        self.display.blit(self.texts[self.current_index], (40, 10))
        match self.current_index:
            case 0:
                for i in range(6):
                    self.display.blit(self.match_leaderboards[i].text_nr, 
                                      self.match_leaderboards[i].dest)
                    self.display.blit(self.match_leaderboards[i].text_name, 
                                      (self.match_leaderboards[i].dest[0] + 40, self.match_leaderboards[i].dest[1]))
                    self.display.blit(self.match_leaderboards[i].text_score, 
                                      (self.match_leaderboards[i].dest[0] + 180, self.match_leaderboards[i].dest[1]))
            case 1:
                for i in range(6):
                    self.display.blit(self.simonsays_leaderboards[i].text_nr, 
                                      self.simonsays_leaderboards[i].dest)
                    self.display.blit(self.simonsays_leaderboards[i].text_name, 
                                      (self.simonsays_leaderboards[i].dest[0] + 40, self.simonsays_leaderboards[i].dest[1]))
                    self.display.blit(self.simonsays_leaderboards[i].text_score, 
                                      (self.simonsays_leaderboards[i].dest[0] + 180, self.simonsays_leaderboards[i].dest[1]))
            case 2:
                for i in range(6):
                    self.display.blit(self.minesweeper_leaderboards[i].text_nr, 
                                      self.minesweeper_leaderboards[i].dest)
                    self.display.blit(self.minesweeper_leaderboards[i].text_name, 
                                      (self.minesweeper_leaderboards[i].dest[0] + 40, self.minesweeper_leaderboards[i].dest[1]))
                    self.display.blit(self.minesweeper_leaderboards[i].text_score, 
                                      (self.minesweeper_leaderboards[i].dest[0] + 180, self.minesweeper_leaderboards[i].dest[1]))

        pygame.display.update()
        self.was_updated = False
