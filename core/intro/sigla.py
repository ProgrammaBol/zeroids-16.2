# _*_ coding: utf-8 _*_

import pygame
import sys
import os
from astronave import Astronave
import strumenti
from strumenti import Attore, Timer
from pianeta import Pianeta
import random

max_fps = 25
clock = pygame.time.Clock()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            return False
    return True


def intro_title(screen, game_context):
    title_font_path = os.path.normpath("assets/font/Dosis-ExtraBold.otf")
    title_font = pygame.font.Font(title_font_path, 170)

    titolo = title_font.render("Zeroids", 1, (255, 100, 0), (0, 0, 0))
    titolo.set_alpha(5)
    titolo_black = title_font.render("Zeroids", 1, (250, 100, 0))

    rect_titolo = titolo.get_rect()
    rect_base = rect_titolo.copy()
    rect_base.center = (game_context.resolution[0]/2, game_context.resolution[1]/2)
    cont = True
    i = 125
    while cont and i > 0:
        cont = handle_events()
        if i < 75:
            rect_titolo.center = (
                rect_base.center[0] + random.randint(-7, 8),
                rect_base.center[1] + random.randint(-8, 7)
            )
            screen.blit(titolo, rect_titolo)
        i = i - 1
        screen.blit(titolo, rect_base)
        pygame.display.flip()
        clock.tick(max_fps)


def fade_to_black(window_size, screen):
    black = pygame.Surface(window_size, pygame.SRCALPHA)
    black.fill((0, 0, 0, 5))
    for i in range(1, 55):
        handle_events()
        screen.blit(black, (0, 0))
        pygame.display.flip()
        clock.tick(max_fps)


def fade_to_background(window_size, screen):
    black = pygame.Surface(window_size, pygame.SRCALPHA)
    black.fill((0, 0, 0, 5))
    for i in range(1, 51):
        handle_events()
        screen.blit(black, (0, 0))
        pygame.display.flip()
        clock.tick(max_fps)


def typeText(testo, dimensione, colore):
    font_path = os.path.normpath("assets/font/Dosis-Regular.otf")
    font = pygame.font.Font(font_path, dimensione)
    return font.render(testo, 1, colore)


def personaggi_entrano_in_scena(screen, game_context):

    personaggi = pygame.sprite.LayeredDirty()

    sfondo = Pianeta()
    personaggi.add(sfondo)

    navetta = Astronave()
    navetta.teleport(20, 300)
    personaggi.add(navetta)

    cucciolo = Attore()
    cucciolo.costume_da_file(os.path.normpath("assets/images/astro_baby_c3.png"))
    cucciolo.costume_da_file(os.path.normpath("assets/images/astro_baby_c8.png"))
    cucciolo.spostati_a(650, 0)
    personaggi.add(cucciolo)

    master = Attore()
    master.costume_da_file(os.path.normpath("assets/images/boss_asteroide.png"))
    master.spostati_a(650, 0)
    master.orientation_mode = strumenti.ORIENTATION_COSTUME_FLIP_H
    personaggi.add(master)


    click_continue = Attore()
    click_continue.costume(typeText("Click to SKIP >>", 24, (255, 255, 0)))
    movex = game_context.resolution[0] - click_continue.rect.width
    movey = game_context.resolution[1] - click_continue.rect.height
    #click_continue.spostati_a(720, 575)
    click_continue.spostati_a(movex, movey)
    personaggi.add(click_continue)

    sequenza = Timer()
    sequenza.add(0, cucciolo, "nascondi")
    sequenza.add(0, master, "nascondi")

    sequenza.add(100, navetta, "speed_", 2, 0)
    sequenza.add(7000, navetta, "speed_", 0, 0)
    sequenza.add(1500, cucciolo, "spostati_a", 100, 100)
    sequenza.add_after(550, cucciolo, "velocita", 5)
    sequenza.add_chain(1, cucciolo, "cambia_visibilita")
    sequenza.add_chain(1000, cucciolo, "direzione", 45)
    sequenza.add_chain(1000, cucciolo, "set_angolo", 75)
    sequenza.add_chain(50, cucciolo, "ruota", -5)
    sequenza.add_chain(2500, cucciolo, "velocita", 0)
    sequenza.add_chain(500, navetta, "guarda_verso", cucciolo)
    sequenza.add_chain(50, master, "mostra")
    sequenza.add_chain(50, master, "direzione", 90)
    sequenza.add_chain(500, master, "velocita", 1)
#    sequenza.add_chain(1000, cucciolo, "guarda_verso", (0, 100))
#    sequenza.add_chain(2000, cucciolo, "guarda_verso", (100, 0))
#    sequenza.add_chain(2000, cucciolo, "guarda_verso", (500, 100))
#    sequenza.add_chain(2000, cucciolo, "guarda_verso", (100, 200))


    sequenza.add_after(3000, cucciolo, "ruota", 0)
    sequenza.add_after(500, cucciolo, "usa_costume", 1)

#    sequenza.add_chain(50, cucciolo, "guarda_verso", (100,100))

    cont = True
    while cont:
        #screen.blit(background_image,(0,0))
        cont = handle_events()
        # somma sempre 5 punti di alfa alla  precedente immagine
        sequenza.esegui()
        screen.fill((0,0,0))
        for sprite in personaggi:
            sprite.update()
        personaggi.draw(screen)
        pygame.display.update() # flip()
        clock.tick(max_fps)
