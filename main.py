import pygame
import sys
from astronave import Astronave

resolution = (800,600)
screen = pygame.display.set_mode(resolution)
elements = pygame.sprite.Group()
player_one = Astronave()

elements.add(player_one)

def game_controller():
    return True

def elements_update(elements):
    for element in elements:
        element.update()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_one.speed = 10
            if event.key == pygame.K_RIGHT:
                player_one.angular_speed = 5
            if event.key == pygame.K_LEFT:
                player_one.angular_speed = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_one.speed = 0
            if event.key == pygame.K_RIGHT:
                player_one.angular_speed = 0
            if event.key == pygame.K_LEFT:
                player_one.angular_speed = 0

clock = pygame.time.Clock()
cont = True 
while cont:
    screen.fill((100,150,100))
    handle_events()
    cont = game_controller()
    elements_update(elements)
    elements.draw(screen)
    pygame.display.flip()
    clock.tick(25)
