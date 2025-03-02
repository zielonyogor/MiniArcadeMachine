import os
from time import sleep
import pygame

# os.environ["SDL_VIDEODRIVER"] = "fbcon"
# os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["XDG_RUNTIME_DIR"] = "/tmp"

pygame.init() # look for errors on the console

lcd = pygame.display.set_mode((320, 240))
lcd.fill((255,0,0))

while True:
    print("Waiting...")
    sleep(2)