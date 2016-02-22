from gamecontroller import game_controller
import pygame
import sys

resolution = (800,600)
screen = pygame.display.set_mode(resolution)
elements = pygame.sprite.Group()

def elements_update(elements):
    for element in elements:
        element.update()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

game_status = "init"
cont = True
while cont:
    handle_events()
    cont, elements = game_controller(game_status, elements)
    elements_update(elements)
    elements.draw(screen)
    pygame.display.flip()
