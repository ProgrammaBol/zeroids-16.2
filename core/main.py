import pygame
import os

from datastructures import EventQueue, GameContext
from gamecontroller import GameController
from colorlog import log

tilemap = dict()


def main():
    resolution = (1200, 800)
    max_fps = 50
    default_backcolor = (0, 0, 0)
    pygame.init()

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    filename = os.path.normpath("assets/images/stars.jpg")
    image = pygame.image.load(filename)
    background_image = image.subsurface((0,0), (resolution[0], resolution[1])).copy()
    background_image.convert()
    background_image.set_alpha(127)

    main_event_queue = EventQueue()
    clock = pygame.time.Clock()
    context_data = { "clock": clock,
                     "resolution": resolution,
                     "screen": screen,
                    }
    game_context = GameContext(context_data)
    game_controller = GameController(main_event_queue, game_context)
    loop = True
    clock.tick(max_fps)
    clock.tick(max_fps)
    while loop:
        loop = main_event_queue.handle_events()
        background_change, background, screen_elements = game_controller.update()
        screen.fill(default_backcolor)
        screen.blit(background_image, (0,0))
        screen_elements.draw(screen)
        pygame.display.flip()
        clock.tick(max_fps)

pygame.quit()
