import pygame
import math
import time
from sprites import MovingSprite, StaticSprite
from animations import Animation
from exceptions import AnimationEnded

class Bullet(MovingSprite):

    def __init__(self, game_context, parent=None, initdata={}, random_ranges=None, *group):
        self.costumes = dict()
        self.costumes_defs = dict()
        self.animations = {}
        self.costumes_defs["default"] = ("main", (110, 220, 3, 3))
        self.animations["explode"] = Animation(game_context, self, "explode")
        explode_seq = [
            ("main", (470, 117, 60, 60)),
            ("main", (477, 65, 40, 40)),
            ("main", (481, 28, 35, 35)),
            ("main", (470, 20, 1, 1)),
        ]
        self.animations["explode"].add_sequence(explode_seq, 500, equal_time=True, defs=True)
        super(Bullet, self).__init__(game_context, *group)
        self.deceleration = False
        self.border_action = "destroy"
        self.start_speed = 200
        self.collision_entity = "salve"
        self.parent = parent
        self.parent_class = None
        self.soundslib = game_context.sounds

    def good_hit(self):
        self.speed_x = 0
        self.speed_y = 0
        self.status = "exploding"
        self.collision_entity = "explosion"
        self.soundslib.single_play("gunblast")

    def handle_collision(self, sprite):
        if sprite.parent is self.parent:
            return
        if sprite.collision_entity == "salve" and sprite.parent is self.parent:
            return
        self.good_hit()

    def update(self):
        if self.status == "exploding":
            try:
                self.animations["explode"].update()
            except:
                self.status = "exploded"
            if self.active_costume_name == "destroyed":
                self.status = "exploded"
        else:
            super(Bullet, self).update()
        if self.status == "exploded":
            self.destroyed = True


class Gun(object):

    def __init__(self):
        self.ammo_class = Bullet
        self.fire_rate = 1
        self.autofire = 0
        self.ammo = "projectile"
        self.soundname = "gunshot"


class Laser(StaticSprite):

    def __init__(self, game_context, parent=None, initdata={}, random_ranges=None, *group):
        self.costumes = dict()
        self.parent = None
        self.parent_class = None
        self.game_context = game_context
        self.animations = {}
        initdata['immutable'] = False
        self.parent = initdata.get('parent', None)
        self.target = initdata.get('target', None)
        self.collision_entity = "salve"
        self.soundslib = game_context.sounds
        #self.angle = initdata['angle']
        # find angle
        distancex = self.parent.centerx - self.target[0]
        distancey = self.parent.centery - self.target[1]
        self.ray_angle = (math.degrees(math.atan2(distancey, distancex))- 90) % 360
        m = distancey/distancex
        q = self.parent.centery - m * self.parent.centerx
        # find angle intervals
        distancex = self.parent.centerx
        distancey = self.parent.centery
        topleft = (math.degrees(math.atan2(distancey, distancex)) - 90) % 360
        distancex = self.parent.centerx
        distancey = self.parent.centery - game_context.resolution[1]
        bottomleft = (math.degrees(math.atan2(distancey, distancex)) - 90) % 360
        distancex = self.parent.centerx - game_context.resolution[0]
        distancey = self.parent.centery
        topright = (math.degrees(math.atan2(distancey, distancex)) - 90) % 360
        distancex = self.parent.centerx - game_context.resolution[0]
        distancey = self.parent.centery - game_context.resolution[1]
        bottomright = (math.degrees(math.atan2(distancey, distancex)) - 90) % 360
        if self.ray_angle >= topleft or (self.ray_angle > 0 and self.ray_angle < topright):
            y = 0
            x = (y - q)/m
        if self.ray_angle >= topright and self.ray_angle < bottomright:
            x = game_context.resolution[0]
            y = m * x + q
        if self.ray_angle >= bottomright and self.ray_angle < bottomleft:
            y = game_context.resolution[1]
            x = (y - q)/m
        if self.ray_angle >= bottomleft and self.ray_angle < topleft:
            x = 0
            y = m * x + q
        self.m = m
        self.q = q
        self.ray_x = x
        self.ray_y = y
        if self.ray_x > self.parent.centerx:
            posx = self.parent.centerx
        else:
            posx = self.ray_x
        width = abs(self.ray_x - self.parent.centerx)
        if self.ray_y > self.parent.centery:
            posy = self.parent.centery
            height = self.ray_y - self.parent.centery
        else:
            posy = self.ray_y
            height = self.parent.centery - self.ray_y
        initdata['centerx'] = posx + width/2
        initdata['centery'] = posy + height/2
        self.ray_duration = 500
        self.costumes["default"] = pygame.Surface((width,height))
        self.costumes['default'].set_alpha(0)
        super(Laser, self).__init__(game_context, initdata=initdata, *group)
        self.shape = "line"
        self.costumes['default'].set_colorkey((0,0,0))
        self.animations["ray"] = Animation(game_context, self, "ray")
        widths = range(1,6) + range(6,0,-1)
        radiuses = range(1,8)
        frame_duration = self.ray_duration/(len(widths) + len(radiuses))
        for radius in radiuses:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.circle(image, (255,255,255), (self.parent.rect.centerx, self.parent.rect.centery), radius)
            self.animations['ray'].add_frame(image, duration_msec=frame_duration, defs=False)
        for ray_width in widths:
            image = self.costumes['default'].copy()
            if ray_width == 1:
                image.set_alpha(0)
            else:
                image.set_alpha(127)
            if m > 0:
                pygame.draw.line(image, (255,255,255), (0,0), (width,height), ray_width)
            else:
                pygame.draw.line(image, (255,255,255), (0,height), (width,0), ray_width)

            self.animations['ray'].add_frame(image, duration_msec=frame_duration, defs=False)
        self.change_active_costume('default')


    def good_hit(self, sprite):
        # accorcia il laser fino al primo sprite colpito
        #self.soundslib.single_play("gunblast")
        self.ray_x = self.collision_points[sprite][0]
        self.ray_y = self.collision_points[sprite][1]
        self.animations["ray"] = Animation(self.game_context, self, "ray")
        widths = range(1,6) + range(6,0,-1)
        radiuses = range(1,8)
        frame_duration = self.ray_duration/(len(widths) + len(radiuses))
        for radius in radiuses:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.circle(image, (255,255,255), (self.parent.rect.centerx, self.parent.rect.centery), radius)
        for width in widths:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.line(image, (255,255,255), (self.parent.centerx,self.parent.centery), (self.ray_x,self.ray_y), width)
            pygame.draw.circle(image, (255,255,255), (self.ray_x, self.ray_y), 8)
            self.animations['ray'].add_frame(image, duration_msec=frame_duration, defs=False)
        self.change_active_costume('default')

    def handle_collision(self, sprite):
        if sprite is not self.parent:
            #trova lo sprite piu' vicino
            self.good_hit(sprite)

    def update(self):
        super(Laser, self).update()
        try:
            self.animations["ray"].update()
        except AnimationEnded:
            self.destroyed = True


class LaserGun(object):

    def __init__(self):
        self.ammo_class = Laser
        self.fire_rate = 1
        self.autofire = 0
        self.ammo = "laser"
        self.soundname = "gunshot"
