import pygame

from datastructures import EventQueue, GameContext
from gamecontroller import GameController
from colorlog import log

tilemap = dict()


def main():
    resolution = (1200, 800)
    max_fps = 50
    default_backcolor = (50, 10, 0)
    pygame.init()

    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    main_event_queue = EventQueue()
    clock = pygame.time.Clock()
    context_data = { "clock": clock,
                     "resolution": resolution,
                     "screen": screen,
                    }
    game_context = GameContext(context_data)
    game_controller = GameController(main_event_queue, game_context)
    game_controller.initgame()
    loop = True
    clock.tick(max_fps)
    clock.tick(max_fps)
    while loop:
        loop = main_event_queue.handle_events()
        background_change, background, screen_elements = game_controller.update()
        screen.fill(default_backcolor)
        #background.draw(screen)
        screen_elements.draw(screen)
        pygame.display.flip()
        clock.tick(max_fps)

pygame.quit()
