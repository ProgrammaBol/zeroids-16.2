import pygame
import os

class Pianeta(pygame.sprite.DirtySprite):
    
    def __init__(self, *group):
        super(Pianeta, self) .__init__(*group)
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0
        self.base = pygame.image.load(os.path.normpath("assets/images/space_1.png"))
        self.base = self.base.convert()
        self.image= self.base
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
   

    def move(self):
        self.speed_x = -5

        if self.centerx < 100 : self.speed_x = 0


        self.centerx = self.centerx + self.speed_x
        self.centery = self.centery + self.speed_y
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        
        
    def update(self):
        self.move()
        self.dirty = 1
