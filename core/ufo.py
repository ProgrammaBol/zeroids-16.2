import math
import pygame
import random
from sprites import MovingSprite
from animations import Animation
from weapons import Gun



class UfoShip(MovingSprite):

    def __init__(self, game_context, parent=None, initdata=None, *group):
        self.costumes = dict()
        self.costumes_defs = dict()
        self.costumes_defs["default"] = ("main", (92, 159, 28, 23))
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
        super(UfoShip, self).__init__(game_context, *group)
        self.deceleration = False
        self.collision_entity = "mob"
        self.angular_speed = 0
        self.start_speed = initdata["speed"]
        self.centerx = initdata["centerx"]
        self.centery = initdata["centery"]
        self.direction = initdata["direction"]
        self.parent = parent
        self.border_action = "bounce"
        self.ai_eval_time = 2000
        self.ai_countdown = self.ai_eval_time
        self.max_speed = 150
        self.targets = initdata['targets']

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
            maintain_speed = random.choice([0,1])
            if not maintain_speed:
                self.change_speed(random.randrange(50,self.max_speed, 30))
            maintain_direction = random.choice([0,1])
            if not maintain_direction:
                self.change_direction(random.randrange(0,359))
            self.ai_countdown = self.ai_eval_time
            fire = random.choice([0,1])
            if fire:
                self.parent.shoot()


    def setup_ai(self, scheme):
        self.ai_scheme = scheme
        self.angle = 0

    def update(self):
        if self.status == "exploding":
            try:
                self.animations["explode"].update()
            except:
                self.status = "exploded"
        else:
            self.ai_move()
            super(UfoShip, self).update()
        if self.status == "exploded":
            self.destroyed = True

class Ufo(pygame.sprite.Group):

    def __init__(self, game_context, initdata=None, *group):
        super(Ufo, self).__init__()
        self.spriteslib = game_context.sprites
        self.main_sprite = self.spriteslib.get_sprite(UfoShip, game_context, initdata=initdata, parent=self)
        self.add(self.main_sprite)
        self.weapons = dict()
        self.weapons["gun"] = Gun()
        self.current_weapon = self.weapons["gun"]
        self.soundslib = game_context.sounds
        self.game_context = game_context
        self.targets = initdata['targets']

    def shoot(self):
        ammo_sprite = self.spriteslib.get_sprite(self.current_weapon.ammo_class, self.game_context, parent=self)
        ammo_sprite.owner = self.main_sprite
        target = random.choice(self.targets)
        distancex = self.main_sprite.centerx - target.centerx
        distancey = self.main_sprite.centery - target.centery
        ammo_sprite.direction = math.degrees(math.atan2(distancey, distancex)) - 90
        ammo_sprite.centerx = self.main_sprite.centerx
        ammo_sprite.centery = self.main_sprite.centery
        self.soundslib.single_play(self.current_weapon.soundname)
        self.add(ammo_sprite)

