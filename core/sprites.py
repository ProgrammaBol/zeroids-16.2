import pygame
import math
import random

class SpritesLib(object):

    def __init__(self, game_context):
        self.sheets = dict()
        self.soundslib = game_context.sounds
        self.clock = game_context.clock
        self.resolution = game_context.resolution

    def load_sheet(self, name):
        if type(self.sheets[name]) != pygame.Surface:
            filename, colorkey = self.sheets[name]
            sheet_raw = pygame.image.load(filename)
            sheet = sheet_raw.convert()
            if colorkey:
                sheet.set_colorkey(colorkey)
            self.sheets[name] = sheet
        return self.sheets[name]

    def add_sheet(self, name, filename, colorkey):
        self.sheets[name] = (filename, colorkey)

    def get_image(self, sheet_name, rect):
        spritesheet = self.load_sheet(sheet_name)
        spriteimage = spritesheet.subsurface(rect).copy()
        return spriteimage

    def get_sprite(self, sprite_class, game_context, parent=None, initdata={}, random_ranges=None):
        sprite = sprite_class(game_context, parent=parent, initdata=initdata, random_ranges=random_ranges)
        if hasattr(sprite, "costumes_defs"):
            for costume_name, costume_definition in sprite.costumes_defs.items():
                costume_position = costume_definition
                costume_sheet = costume_position[0]
                costume_rect = costume_position[1]
                costume_image = self.get_image(costume_sheet, costume_rect)
                sprite.costumes[costume_name] = costume_image
        sprite.change_active_costume(sprite.active_costume_name)
        return sprite

class StaticSprite(pygame.sprite.Sprite):

    def __init__(self, game_context, initdata={}, random_ranges=None, *group):
        super(StaticSprite, self).__init__(*group)
        self.game_context = game_context
        if random_ranges:
            initdata = self.generate_random_init(random_ranges)
        self.centerx = 0.0
        self.centerx = initdata.get('centerx', 0.0)
        self.centery = initdata.get('centery', 0.0)
        self.visible = False
        self.masks = dict()
        self.active_costume_name = "default"
        self.angle = 0
        self.active_collisions = pygame.sprite.OrderedUpdates()
        self.collision_points = {}
        self.handled_collisions = pygame.sprite.OrderedUpdates()
        self.shape = "rect"
        self.immutable = initdata.get("immutable", False)
        self.destroyed = False
        self.clock = game_context.clock

    def generate_random_init(self, ranges):
        centerx_min = ranges.get('centerx_min', 0)
        centerx_max = ranges.get('centerx_max', self.game_context.resolution[0])
        centery_min = ranges.get('centery_min', 0)
        centery_max = ranges.get('centery_max', self.game_context.resolution[1])
        position_allowed_borders = ranges.get('position_allowed_borders', ["top", "bottom", "left", "right"])
        position_type = ranges['position_type']
        centerx = random.randint(centerx_min, centerx_max)
        centery = random.randint(centery_min, centery_max)
        if position_type == "offmap":
            border = random.choice(position_allowed_borders)
            if border == "top":
                centery = 0
            elif border == "bottom":
                centery = self.resolution[1]
            elif border == "left":
                centerx = 0
            elif border == "right":
                centery = self.resolution[0]
        init = {}
        init['centerx'] = centerx
        init['centery'] = centery
        return init

    def change_active_costume(self, costume_name):
        self.image = self.costumes[costume_name]
        rect = self.costumes[costume_name].get_rect()
        rect.centerx = self.centerx
        rect.centery = self.centery
        self.rect = rect
        #self.mask = self.masks[costume_name]

    def rotate(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.costumes[self.active_costume_name],  - self.angle)
        self.rect.size = self.image.get_rect().size
        self.rect.center = center

    def update(self):
        self.image = self.costumes[self.active_costume_name]
        self.rotate()
        # Clear collided sprite from handled if it's not active collisino anymore
        for sprite in self.handled_collisions.sprites():
            if sprite not in self.active_collisions:
                self.handled_collisions.remove(sprite)
                #del(self.collision_points[sprite])
        # Handle active collision if they've already handled
        if self.active_collisions:
            for sprite in self.active_collisions.sprites():
                if sprite not in self.handled_collisions:
                    self.handle_collision(sprite)
                    self.handled_collisions.add(sprite)

class MovingSprite(StaticSprite):

    def __init__(self, game_context, initdata={}, random_ranges=None, *group):
        super(MovingSprite, self).__init__(game_context, initdata=initdata, random_ranges=random_ranges, *group)
        if random_ranges:
            initdata = self.generate_random_init(random_ranges)
        getattr(self, "max_speed", 0)
        getattr(self, "start_speed", 0)
        self.start_speed = initdata.get('start_speed', 0)
        self.direction = initdata.get('direction', 0)
        # speeds are in unit/sec
        self.angular_speed = 0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.acceleration = 0.0
        self.deceleration = 0.9
        self.gravity_direction = 0
        self.gravity_force = 0
        self.status = "stop"
        self.immutable = False
        # DESTROY, BOUNCE, ROUNDRIBBON
        self.border_action = "roundribbon"
        self.ai_scheme = None
        self.resolutionx, self.resolutiony = game_context.resolution
        self.angle_is_direction = False

    def generate_random_init(self, ranges):
        speed_min = ranges['speed_min']
        speed_max = ranges['speed_max']
        direction_min = ranges['direction_min']
        direction_max = ranges['direction_max']
        direction = random.randint(direction_min, direction_max)
        speed = random.randint(speed_min, speed_max)
        init = {}
        init['start_speed'] = speed
        init['direction'] = direction
        return init


    def spin(self):
        frame_msec = self.clock.get_time()
        increment_perframe = float(frame_msec * self.angular_speed) / 1000
        self.angle = (self.angle + increment_perframe) % 360
        if self.angle_is_direction == True:
            self.direction = self.angle

    def accelerate(self, x_component, y_component):
        frame_msec = self.clock.get_time()
        t = frame_msec/1000.0
        increment_perframe = float(frame_msec * self.acceleration) / 1000
        max_speed_x = abs(self.max_speed * x_component)
        max_speed_y = abs(self.max_speed * y_component)
        acceleration_x = self.acceleration * x_component * t
        acceleration_y = self.acceleration * y_component * t
        self.speed_x = self.speed_x + acceleration_x
        if abs(self.speed_x) > max_speed_x:
            self.speed_x = self.speed_x - acceleration_x
        self.speed_y = self.speed_y + acceleration_y
        if abs(self.speed_y) > max_speed_y:
            self.speed_y = self.speed_y - acceleration_y

    def decelerate(self, x_component, y_component):
        frame_msec = self.clock.get_time()
        t = 1000.0/frame_msec
        p = 1.000/t
        deceleration = math.pow(self.deceleration, p)
        if self.speed_x != 0:
            self.speed_x = self.speed_x * deceleration
            if abs(self.speed_x) < .05:
                self.speed_x = 0
        if self.speed_y != 0:
            self.speed_y = self.speed_y * deceleration
            if abs(self.speed_y) < .05:
                self.speed_y = 0

    @property
    def speed(self):
        return math.sqrt(self.speed_x**2 + self.speed_y**2)

    def move(self):
        frame_msec = self.clock.get_time()
        increment_perframe = float(frame_msec * self.speed_x) / 1000
        self.centerx = self.centerx + increment_perframe
        increment_perframe = float(frame_msec * self.speed_y) / 1000
        self.centery = self.centery + increment_perframe
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def apply_gravity(self):
        pass

    def change_direction(self, direction):
        self.direction = direction
        if self.angle_is_direction:
            self.angle = direction
        current_speed = self.speed
        x_component = round(math.sin(math.radians(self.direction)), 8)
        y_component = round((-math.cos(math.radians(self.direction))), 8)
        self.speed_x = current_speed * x_component
        self.speed_y = current_speed * y_component

    def change_speed(self, speed):
        x_component = round(math.sin(math.radians(self.direction)), 8)
        y_component = round((-math.cos(math.radians(self.direction))), 8)
        self.speed_x = speed * x_component
        self.speed_y = speed * y_component

    def update(self):
        # borders
        if self.centerx > self.resolutionx and self.direction in range(1,179):
            if self.border_action == "roundribbon":
                self.centerx = -self.rect.width
            elif self.border_action == "destroy":
                self.destroyed = True
            elif self.border_action == "bounce":
                self.change_direction(- self.direction % 360)
        elif self.centerx < 0 and self.direction in range(181,359):
            if self.border_action == "roundribbon":
                self.centerx = self.resolutionx
            elif self.border_action == "destroy":
                self.destroyed = True
            elif self.border_action == "bounce":
                self.change_direction(- self.direction % 360)
        if self.centery > self.resolutiony and self.direction in range(91, 269):
            if self.border_action == "roundribbon":
                self.centery = -self.rect.height
            elif self.border_action == "destroy":
                self.destroyed = True
            elif self.border_action == "bounce":
                self.change_direction((180 - self.direction) % 360)
        elif self.centery < 0 and (self.direction in range(0,89) or self.direction in range(271,359)):
            if self.border_action == "roundribbon":
                self.centery = self.resolutiony
            elif self.border_action == "destroy":
                self.destroyed = True
            elif self.border_action == "bounce":
                self.change_direction((180 - self.direction) % 360)
        if self.angular_speed != 0:
            self.spin()
        super(MovingSprite, self).update()
        x_component = round(math.sin(math.radians(self.direction)), 8)
        y_component = round((-math.cos(math.radians(self.direction))), 8)
        if self.start_speed:
            self.speed_x = self.start_speed * x_component
            self.speed_y = self.start_speed * y_component
            self.start_speed = 0
        if self.acceleration:
            self.accelerate(x_component, y_component)
        if self.deceleration:
            self.decelerate(x_component, y_component)
        if self.gravity_force:
            self.apply_gravity()
        self.move()
