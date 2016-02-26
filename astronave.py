import pygame
import math

class Astronave(pygame.sprite.Sprite):
    
    def __init__(self, *group):
        super(Astronave, self).__init__(*group)
        self.angle = 0
        self.angular_speed = 0
        self.speed = 0
        self.centerx = 50.0
        self.centery = 50.0
	image = pygame.Surface((10,10))
        image.fill((255,0,0))
	self.base_image = image
        self.rect = image.get_rect()

    def rotate(self):
        if self.angular_speed != 0:
	    self.angle = (self.angle + self.angular_speed) % 360
        center = self.rect.center
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect.size = self.image.get_rect().size
        self.rect.center = center

    def move(self, speed_x, speed_y):
        self.centerx = self.centerx + speed_x
        self.centery = self.centery + speed_y
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def update(self):
        self.rotate()
        x_component = round(math.sin(math.radians(self.angle)), 8)
        y_component = round((-math.cos(math.radians(self.angle))), 8)
        speed_x = self.speed * x_component
        speed_y = self.speed * y_component
        self.move(speed_x, speed_y)
