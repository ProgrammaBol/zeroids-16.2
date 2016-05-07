import pygame
from sprites import MovingSprite, StaticSprite
from animations import Animation
from exceptions import AnimationEnded

class Bullet(MovingSprite):

    def __init__(self, game_context, parent=None, initdata={}, random_ranges={}, *group):
        self.game_context = game_context
        self.costumes = dict()
        self.costumes_defs = dict()
        self.animations = {}
        self.costumes_defs["default"] = ("main", (110, 220, 3, 3))
        self.animations["explode"] = self.game_context.animations.get_animation(self, "bulletexplode", 0)
        super(Bullet, self).__init__(game_context, *group)
        self.deceleration = False
        self.border_action = "destroy"
        self.start_speed = 200
        self.collision_entity = "salve"
        self.parent = parent
        self.parent_class = None

    def good_hit(self):
        self.speed_x = 0
        self.speed_y = 0
        self.status = "exploding"
        self.collision_entity = "explosion"

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

    def __init__(self, game_context, parent=None, initdata={}, random_ranges={}, *group):
        self.costumes = dict()
        self.parent = parent
        self.parent_class = None
        self.game_context = game_context
        self.animations = {}
        self.target = initdata['target']
        initdata['immutable'] = False
        self.m = initdata.get('m', 0)
        self.q = initdata.get('q', 0)
        self.collision_entity = "salve"
        self.ray_x = initdata.get('borderx', 0)
        self.ray_y = initdata.get('bordery', 0)
        self.hit = False
        initdata['angle'] = None
        self.ray_duration = 500
        initdata['centerx'] = game_context.resolution[0]/2
        initdata['centery'] = game_context.resolution[1]/2
        self.costumes["default"] = pygame.Surface((game_context.resolution[0], game_context.resolution[1]))
        self.costumes['default'].set_alpha(0)
        super(Laser, self).__init__(game_context, initdata=initdata, *group)
        self.shape = "line"
        self.costumes['default'].set_colorkey((0,0,0))
        self.prepare_animation()

    def prepare_animation(self, hit=False):
        rangestart = 1
        if hit:
            rangestart += 1
            self.animations["ray"].count=1
        else:
            self.animations["ray"] = Animation(self.game_context, self, "ray")
        widths = range(rangestart,6) + range(6,0,-1)
        radiuses = range(1,8)
        frame_duration = self.ray_duration/(len(widths) + len(radiuses))
        for radius in radiuses:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.circle(image, (255,255,255), (self.parent.rect.centerx, self.parent.rect.centery), radius)
            self.animations['ray'].append_frame(image, duration_msec=frame_duration, defs=False)
        for ray_width in widths:
            image = self.costumes['default'].copy()
            if ray_width == 1:
                image.set_alpha(0)
            else:
                image.set_alpha(127)
            pygame.draw.line(image, (255,255,255), (self.parent.rect.centerx,self.parent.rect.centery), (self.ray_x, self.ray_y), ray_width)
            if hit:
                pygame.draw.circle(image, (255,255,255), (self.ray_x, self.ray_y), 8)

            self.animations['ray'].append_frame(image, duration_msec=frame_duration, defs=False)
        self.change_active_costume('default')

    def good_hit(self):
        # accorcia il laser fino al primo sprite colpito
        self.prepare_animation(hit=True)

    def nada(self):
        self.animations["ray"] = Animation(self.game_context, self, "ray")
        widths = range(2,6) + range(6,0,-1)
        radiuses = range(1,8)
        frame_duration = self.ray_duration/(len(widths) + len(radiuses))
        for radius in radiuses:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.circle(image, (255,255,255), (self.ray_sourcex, self.parent.rect.centery), radius)
        for width in widths:
            image = self.costumes['default'].copy()
            image.set_alpha(127)
            pygame.draw.line(image, (255,255,255), (self.parent.rect.centerx,self.parent.rect.centery), (self.ray_x,self.ray_y), width)
            self.animations['ray'].add_frame(image, duration_msec=frame_duration, defs=False)
        self.change_active_costume('default')

    def handle_collision(self, sprite):
        if sprite is not self.parent and sprite.collision_entity is not "text":
            #trova lo sprite piu' vicino
            self.ray_x = self.rect.x + self.collision_points[sprite][0]
            self.ray_y = self.rect.y + self.collision_points[sprite][1]
            if self.hit == False:
                self.hit = True
                self.good_hit()

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
