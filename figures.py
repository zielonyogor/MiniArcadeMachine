import pygame
from pygame.locals import *
from globals import *


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, size, hex_color):
        super(Square, self).__init__()

        self.surf = pygame.Surface((size, size))
        self.surf.fill(Color(hex_color))

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

class Pointer(pygame.sprite.Sprite):
    def __init__(self, size, rows, columns, offset_x = 30, offset_y = 36, space = 12):
        super(Pointer, self).__init__()

        self.size = size
        self.rows = rows
        self.columns = columns

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.space = space

        self.surf = pygame.Surface((self.size + 8, self.size + 8))
        self.rect = self.surf.get_rect()

        self.current_index = [0, 0]
        self.update_position()
    
    def move(self, x, y):
        self.current_index[0] += y
        self.current_index[0] = 0 if self.current_index[0] == self.columns else self.columns - 1 if self.current_index[0] < 0 else self.current_index[0]
        self.current_index[1] += x
        self.current_index[1] = 0 if self.current_index[1] == self.rows else self.rows - 1 if self.current_index[1] < 0 else self.current_index[1]
        self.update_position()
    
    def update_position(self):
        self.rect.x = self.current_index[1] * (self.size + self.space) + self.offset_x - 4
        self.rect.y = self.current_index[0] * (self.size + self.space) + self.offset_y - 4

