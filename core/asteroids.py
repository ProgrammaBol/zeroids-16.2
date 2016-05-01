import pygame
import random
from sprites import MovingSprite


class AsteroidFragment(MovingSprite):

    def __init__(self, game_context, parent=None, initdata={}, random_ranges={}, *group):
        self.costumes = dict()
        self.costumes_defs = dict()
        self.size = initdata["size"]
        if self.size == 3:
            #self.costumes_defs["default"] = ("main", (302, 20, 50, 43))
            self.costumes_defs["default"] = ("extended", (0, 0, 61, 48))
        elif self.size == 2:
            #self.costumes_defs["default"] = ("main", (274, 125, 23, 28))
            self.costumes_defs["default"] = ("extended", (66, 0, 47, 35))
        elif self.size == 1:
            #self.costumes_defs["default"] = random.choice([("main", (292, 166, 18, 15),)
            self.costumes_defs["default"] = random.choice([("extended", (117, 0, 30, 34)),("extended", (151,0,32,35))])
        self.animations = {}
        self.animations["explode"] = game_context.animations.get_animation(self, "explode", 3)
        super(AsteroidFragment, self).__init__(game_context, initdata=initdata, random_ranges=random_ranges,*group)
        self.deceleration = False
        self.collision_entity = "mob"
        self.angular_speed = 35
        self.parent = parent

    def explode(self):
        self.speed_x = 0
        self.speed_y = 0
        self.status = "exploding"
        #self.soundslib.single_play("gunblast")

    def handle_collision(self, sprite):
        if sprite.collision_entity == "salve":
            if self.size == 1:
                self.explode()
            else:
                self.parent.divide(self)
                self.explode()

    def update(self):
        if self.status == "exploding":
            try:
                self.animations["explode"].update()
            except:
                self.status = "exploded"
        else:
            super(AsteroidFragment, self).update()
        if self.status == "exploded":
            self.destroyed = True
            self.parent.children -= 1

class Asteroid(pygame.sprite.Group):

    def __init__(self, game_context, initdata={}, random_ranges={}, *group):
        super(Asteroid, self).__init__()
        self.spriteslib = game_context.sprites
        initdata["size"] = 3

        self.game_context = game_context
        self.main_sprite = self.spriteslib.get_sprite(AsteroidFragment, game_context, parent=self, initdata=initdata, random_ranges=random_ranges)
        self.add(self.main_sprite)
        self.soundslib = game_context.sounds
        self.children = 1
        self.random_ranges = random_ranges
        #fragment = AsteroidFragment(clock, soundslib, self, size, *group)
        #self.fragments.append(fragment)

    def divide(self, child):
        for i in range(0, 2):
            initdata = {}
            if i == 0: direction = 30
            elif i == 1: direction = -30
            initdata["size"] = child.size - 1
            initdata['direction'] = child.direction + direction
            initdata['centerx'] = child.centerx
            initdata['centery'] = child.centery
            initdata['start_speed'] = child.speed
            fragment = self.spriteslib.get_sprite(AsteroidFragment, self.game_context, parent=self, initdata=initdata)
            self.add(fragment)
            self.children += 1
