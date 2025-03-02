import time
from random import randint

import pygame
from pygame.locals import *

import figures as fig
from game_scene import Scene
from globals import *

SQUARE_SIZE = 64
SIMON_COLOR = '#FFFFFF'
SIMON_SIZE = SQUARE_SIZE + 6


class SimonSays(Scene):

    def __init__(self, display, game_state_manager, font) -> None:
        super().__init__(display, game_state_manager, font)
        # left, right, up, right
        self.squares = [[
            'left',
            fig.Square(8, 100, SQUARE_SIZE, '#FFFF00'),
            fig.Square(5, 97, SIMON_SIZE, SIMON_COLOR)
        ],
                        [
                            'right',
                            fig.Square(160, 100, SQUARE_SIZE, '#0000FF'),
                            fig.Square(157, 97, SIMON_SIZE, SIMON_COLOR)
                        ],
                        [
                            'up',
                            fig.Square(84, 60, SQUARE_SIZE, '#FF0000'),
                            fig.Square(81, 57, SIMON_SIZE, SIMON_COLOR)
                        ],
                        [
                            'down',
                            fig.Square(84, 140, SQUARE_SIZE, '#00FF00'),
                            fig.Square(81, 137, SIMON_SIZE, SIMON_COLOR)
                        ]]

    def enter(self):
        self.time_to_choose = 5
        self.time_before = 0
        self.time_left = 0
        self.score = 0
        self.wrong = -1
        self.state = 'simon'

    def update(self, input):
        if self.state != 'choose':
            return
        if input.type != KEYDOWN:
            return
        if input.key == K_LEFT:
            if self.simon == 0:
                self.win()
            else:
                self.wrong = 0
                self.state = 'lose'
        elif input.key == K_RIGHT:
            if self.simon == 1:
                self.win()
            else:
                self.wrong = 1
                self.state = 'lose'
        elif input.key == K_UP:
            if self.simon == 2:
                self.win()
            else:
                self.wrong = 2
                self.state = 'lose'
        elif input.key == K_DOWN:
            if self.simon == 3:
                self.win()
            else:
                self.wrong = 3
                self.state = 'lose'
        elif input.key == K_z:
            return

    def run(self):
        time_elapsed = time.time() - self.time_before
        self.time_left = self.time_left - time_elapsed
        self.time_before = time.time()

        self.display.fill(pygame.Color('black'))

        match self.state:
            case 'simon':
                self.update_simon()
            case 'choose':
                self.update_choose()
            case 'lose':
                self.update_lose()

        self.update_score()

        pygame.display.update()
        if self.time_left <= 0:
            self.state = 'lose'

    def draw_rectangles(self):
        for i in range(len(self.squares)):
            self.display.blit(self.squares[i][1].surf, self.squares[i][1])

    def update_score(self):
        score_texture = self.font.render(f'Score: {f"{self.score}".zfill(4)}',
                                         False, (255, 255, 255))
        self.display.blit(score_texture, (50, 2))

    def update_simon(self):
        self.draw_rectangles()
        self.simon = randint(0, 3)
        #self.simon = self.squares[ran][0]
        self.time_before = time.time()
        self.time_left = self.time_to_choose
        self.state = 'choose'

    def update_choose(self):
        self.display.blit(self.squares[self.simon][2].surf,
                          self.squares[self.simon][2])

        self.draw_rectangles()

    def win(self):
        self.score = self.score + 1
        if self.time_to_choose >= 0.14:
            self.time_to_choose = self.time_to_choose - 0.1
        self.state = 'simon'

    def update_lose(self):
        lose_texture = self.font.render('You lose', False, (255, 255, 255))
        self.display.blit(lose_texture, (60, 23))
        self.draw_rectangles()
        pygame.draw.circle(
            self.display, '#FFFFFF',
            (self.squares[self.simon][1].rect.x + SQUARE_SIZE / 2,
             self.squares[self.simon][1].rect.y + SQUARE_SIZE / 2), 15, 2)

        #drawing x
        wrong_square = self.squares[self.wrong][1]
        if self.wrong >= 0:
            offset=10
            pygame.draw.line(
                self.display, '#FFFFFF',
                (wrong_square.rect.x+offset, wrong_square.rect.y+offset),
                (wrong_square.rect.x-offset + SQUARE_SIZE, wrong_square.rect.y+SQUARE_SIZE -offset), 2)
            pygame.draw.line(
                self.display, '#FFFFFF',
                (wrong_square.rect.x-offset + SQUARE_SIZE, wrong_square.rect.y+offset),
                (wrong_square.rect.x+offset, wrong_square.rect.y -offset + SQUARE_SIZE), 2)
