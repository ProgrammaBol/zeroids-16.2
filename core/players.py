import pygame

from weapons import Gun

from sprites import MovingSprite


class AlloyShip(MovingSprite):

    def __init__(self, game_context, parent=None, initdata={}, random_ranges=None, *group):
        self.max_speed = 100
        self.costumes = dict()
        self.costumes_defs = dict()
        self.costumes_defs["default"] = ("main", (481, 403, 29, 29))
        self.costumes_defs["thrusting"] = ("main", (481, 358, 29, 29))
        super(AlloyShip, self).__init__(game_context, initdata=initdata, random_ranges=random_ranges, *group)
        self.collision_entity = "player"
        self.soundslib = game_context.sounds
        self.max_angular_speed = 180
        self.angle_is_direction = True
        self.parent = parent
        self.animations = {}
        self.animations["explode"] = game_context.animations.get_animation(self, "explode", 3)

    def rotate_left(self):
        self.angular_speed = -self.max_angular_speed

    def stop_rotate_left(self):
        if self.angular_speed == -self.max_angular_speed:
            self.angular_speed = 0

    def rotate_right(self):
        self.angular_speed = self.max_angular_speed

    def stop_rotate_right(self):
        if self.angular_speed == self.max_angular_speed:
            self.angular_speed = 0

    def thrust_on(self):
        self.thrust_sound_channel = self.soundslib.loop_play("alloyshipthrust")
        self.active_costume_name = "thrusting"
        self.acceleration = 50.0

    def thrust_off(self):
        self.active_costume_name = "default"
        self.acceleration = 0
        self.soundslib.stop_loop(self.thrust_sound_channel)

    def explode(self):
        self.speed_x = 0
        self.speed_y = 0
        self.status = "exploding"

    def handle_collision(self, sprite):
        if sprite.parent is not self.parent:
            self.parent.health -= 50
            if self.parent.health <= 0:
                self.explode()

    def update(self):
        if self.status == "exploding":
            try:
                self.animations["explode"].update()
            except:
                self.status = "exploded"
        else:
            super(AlloyShip, self).update()
        if self.status == "exploded":
            self.destroyed = True

class Player(pygame.sprite.Group):

    def __init__(self, main_sprite_class, game_context, initdata={}, random_ranges=None):
        super(Player, self).__init__()
        self.spriteslib = game_context.sprites
        self.main_sprite = self.spriteslib.get_sprite(main_sprite_class, game_context, initdata=initdata, random_ranges=random_ranges, parent=self)
        self.add(self.main_sprite)
        self.weapons = dict()
        self.weapons["gun"] = Gun()
        self.current_weapon = self.weapons["gun"]
        self.soundslib = game_context.sounds
        self.game_context = game_context
        self.health = 100

    def shoot(self):
        ammo_sprite = self.spriteslib.get_sprite(self.current_weapon.ammo_class, self.game_context, parent=self)
        ammo_sprite.direction = self.main_sprite.direction
        ammo_sprite.centerx = self.main_sprite.centerx
        ammo_sprite.centery = self.main_sprite.centery
        self.soundslib.single_play(self.current_weapon.soundname)
        self.add(ammo_sprite)

    def stop_shooting(self):
        pass

    def keypress_left(self):
        self.main_sprite.rotate_left()

    def keyrelease_left(self):
        self.main_sprite.stop_rotate_left()

    def keypress_right(self):
        self.main_sprite.rotate_right()

    def keyrelease_right(self):
        self.main_sprite.stop_rotate_right()

    def keypress_up(self):
        self.main_sprite.thrust_on()

    def keyrelease_up(self):
        self.main_sprite.thrust_off()

    def keypress_space(self):
        self.shoot()

    def keyrelease_space(self):
        self.stop_shooting()

