import pygame
import math

class Astronave(pygame.sprite.Sprite):
    
    def __init__(self, *group):
        super(Astronave, self).__init__(*group)
        self.heading = 0
        self.angle = 0
        self.angular_speed = 0
        self.speed = 0
        self.rect = pygame.Rect((0,0), (10,10))
        self.centerx = 50.0
        self.centery = 50.0
        self.costumes = dict()
	image = pygame.Surface((10,10))
        image.fill((255,0,0))
	self.costumes["default"] = image
        self.current_costume = "default"

    def rotate(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.costumes[self.current_costume], -self.angle)
        self.rect.size = self.image.get_rect().size
        self.rect.center = center

    def start_rotate(self, angular_speed):
        self.angular_speed = angular_speed

    def stop_rotate(self, direction):
        if direction == "clock" and self.angular_speed > 0:
            self.angular_speed = 0
        elif direction == "counterclock" and self.angular_speed < 0:
            self.angular_speed = 0

    def move(self, speed_x, speed_y):
        self.centerx = self.centerx + speed_x
        self.centery = self.centery + speed_y

    def update(self):
        if self.angular_speed != 0:
	    self.angle = (self.angle + self.angular_speed) % 360
        self.rotate()
        x_component = round(math.sin(math.radians(self.angle)), 8)
        y_component = round((-math.cos(math.radians(self.angle))), 8)
        speed_x = self.speed * x_component
        speed_y = self.speed * y_component
        self.move(speed_x, speed_y)
