import pygame
import math
import random
from sprites import MovingSprite
from animations import Animation
from weapons import LaserGun

class LaserTurret(MovingSprite):

    def __init__(self, game_context, parent=None, initdata=None, *group):
        self.costumes = dict()
        self.costumes_defs = dict()
        self.costumes_defs["default"] = ("main", (26, 292, 29, 29))
        self.animations = {}
        self.animations["explode"] = Animation(game_context, self, "explode")
        explode_seq = [
            ("explode3", (0, 0, 47, 47)),
            ("explode3", (49, 0, 47, 47)),
            ("explode3", (97, 0, 47, 47)),
            ("explode3", (145, 0, 47, 47)),
            ("explode3", (0, 49, 47, 47)),
            ("explode3", (49, 49, 47, 47)),
            ("explode3", (97, 49, 47, 47)),
            ("explode3", (145, 49, 47, 47)),
        ]
        self.animations["explode"].add_sequence(explode_seq, 1000, equal_time=True)
        super(LaserTurret, self).__init__(game_context, *group)
        self.deceleration = False
        self.collision_entity = "mob"
        self.angular_speed = 0
        self.centerx = initdata["centerx"]
        self.centery = initdata["centery"]
        self.parent = parent
        self.ai_eval_time = 2000
        self.ai_countdown = self.ai_eval_time
        self.targets = initdata['targets']
        self.target = random.choice(self.targets)
        self.angle_is_direction = True

    def explode(self):
        self.speed_x = 0
        self.speed_y = 0
        self.status = "exploding"

    def handle_collision(self, sprite):
        if sprite.collision_entity == "salve" and sprite.owner is not self:
            self.explode()

    def ai_move(self):
        #if self.ai_scheme == "default":
        #    pass
        time = self.clock.get_time()
        self.ai_countdown -= time
        if self.ai_countdown <= 0:
            #fire = random.choice([0,1])
            fire = True
            if fire:
                self.parent.shoot()
            self.ai_countdown = self.ai_eval_time

    def setup_ai(self, scheme):
        self.ai_scheme = scheme
        self.angle = 0

    def update(self):
        self.ai_move()
        distancex = self.centerx - self.target.centerx
        distancey = self.centery - self.target.centery
        self.change_direction(math.degrees(math.atan2(distancey, distancex)) - 90)
        super(LaserTurret, self).update()
        if self.status == "exploding":
            try:
                self.animations["explode"].update()
            except:
                self.status = "exploded"
        if self.status == "exploded":
            self.destroyed = True


class Turret(pygame.sprite.Group):

    def __init__(self, game_context, initdata=None, *group):
        super(Turret, self).__init__()
        self.spriteslib = game_context.sprites
        self.main_sprite = self.spriteslib.get_sprite(LaserTurret, game_context, initdata=initdata, parent=self)
        self.add(self.main_sprite)
        self.weapons = dict()
        self.weapons["gun"] = LaserGun()
        self.current_weapon = self.weapons["gun"]
        self.soundslib = game_context.sounds
        self.game_context = game_context
        self.targets = initdata['targets']

    def shoot(self):
        initdata = {}
        initdata['target'] = (self.targets[0].centerx, self.targets[0].centery)
        initdata['owner'] = self.main_sprite
        initdata['centerx'] = self.main_sprite.centerx
        initdata['centery'] = self.main_sprite.centery
        ammo_sprite = self.spriteslib.get_sprite(self.current_weapon.ammo_class, self.game_context, parent=self, initdata=initdata)
        self.soundslib.single_play(self.current_weapon.soundname)
        self.add(ammo_sprite)
