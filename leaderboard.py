import pygame
from pygame.locals import *

import database as db

ICON_SIZE = 64

class Place():
    def __init__(self, x, y, data = None):
        self.text_nr = my_font.render(str(data[0]), False, (255, 255, 255))
        self.text_name = my_font.render(data[1], False, (255, 255, 255))
        self.text_score = my_font.render(str(data[2]), False, (255, 255, 255))
        self.dest = (x, y)
    

# initialize pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("raspberka")

my_font = pygame.font.SysFont('arial', 24)

db.setup()

is_running = True

pygame.display.update()

# db.add_match_2_scores(('freakbear', 2137.77))

match_2_data = db.get_match_2_scores()
scores = []
# F.E. 6 best scores
for i in range(min(6, len(match_2_data))):
    score = Place(10, 10 + 20 * i, (match_2_data[i]))
    scores.append(score)

db.close()


screen.fill(pygame.Color('black'))

for score in scores:
    screen.blit(score.text_nr, score.dest)
    screen.blit(score.text_name, (score.dest[0] + 40, score.dest[1]))
    screen.blit(score.text_score, (score.dest[0] + 200, score.dest[1]))

pygame.display.update()

# here we don't have to update screen cause it doesn't matter
while is_running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                is_running = False
        elif event.type == QUIT:
            is_running = False
    clock.tick(10)