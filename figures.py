import pygame
from pygame.locals import *
from globals import *

SQUARE_SIZE = 36

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, size, hex_color):
        super(Square, self).__init__()

        self.surf = pygame.Surface((size, size))
        self.surf.fill(Color(hex_color))

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

# TODO: change it so that it could be used in 
class Pointer(pygame.sprite.Sprite):
    def __init__(self):
        super(Pointer, self).__init__()

        self.surf = pygame.Surface((SQUARE_SIZE + 8, SQUARE_SIZE + 8))
        self.rect = self.surf.get_rect()

        self.current_index = [0, 0]
        self.update_position()
    
    def move(self, x, y):
        self.current_index[0] += y
        self.current_index[0] = 0 if self.current_index[0] == COLUMNS else COLUMNS - 1 if self.current_index[0] < 0 else self.current_index[0]
        self.current_index[1] += x
        self.current_index[1] = 0 if self.current_index[1] == ROWS else ROWS - 1 if self.current_index[1] < 0 else self.current_index[1]
        self.update_position()
    
    def update_position(self):
        self.rect.x = self.current_index[1] * (COLUMNS + SQUARE_SIZE + 8) + 16 - 4
        self.rect.y = self.current_index[0] * (ROWS + SQUARE_SIZE + 8) + 36 - 4

