import sys
import pygame
from ipwebcam import IPWEBCAM

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((176,144))

ipcam = IPWEBCAM('10.42.0.70:8080') # thats the server address shown on the IP webcam, don't add 'http://' the class adds it

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit()
      sys.exit()
  screen.blit(ipcam.get_pygame_image(),(0,0))
  pygame.display.flip()
  clock.tick(0)