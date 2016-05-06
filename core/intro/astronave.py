import pygame
import strumenti
import os

class Astronave(strumenti.Attore):

    def __init__(self, *group):
        super(Astronave, self) .__init__(*group)
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        spritesheet_path = os.path.normpath("assets/spritesheets/master.png")
        spritesheet_file = pygame.image.load(spritesheet_path)
        main_spritesheet = spritesheet_file.convert()
        main_spritesheet.set_colorkey((0,0,0))
        self.image = main_spritesheet.subsurface((481, 403, 29, 29)).copy()
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.image = pygame.transform.rotate(self.image,-90)

    def move(self):



        #if self.rect.centery <= 20 and self.rect.centerx < 780:
            #self.speed_x = 5
            #self.speed_y = 0
        #elif self.rect.centerx >= 780 and self.rect.centery < 580:
            #self.speed_x = 0
            #self.speed_y = 5
        #elif self.rect.centery >= 580 and self.rect.centerx > 20:
            #self.speed_x = -5
            #self.speed_y = 0
        #elif self.rect.centerx <= 20 and self.rect.centery > 20:
            #self.speed_x = 0
            #self.speed_y = -5

        self.centerx = self.centerx + self.speed_x
        self.centery = self.centery + self.speed_y
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


    def update(self):
        self.move()
        self.dirty = 1


    def teleport(self, x, y):
        self.centerx = x
        self.centery = y



    def speed_(self, x, y):
        self.speed_x = x
        self.speed_y = y

#
#   Metodi aggiunti
#

