import pygame
import os
import pprint
from maps import RoomMap, WorldMap
from asteroids import Asteroid
from sprites import SpritesLib
from players import Player, AlloyShip
from sounds import SoundsLib
from texts import TextLib
from ufo import Ufo
from turret import Turret
# levels (roomid)

def weightedcollide():
    pass


class GameController(object):

    def __init__(self, event_queue, game_context):
        self.players = dict()
        self.status = "start"
        self.worldmap = WorldMap((3, 3))
        self.elements = pygame.sprite.LayeredUpdates()
        self.event_queue = event_queue
        self.clock = game_context.clock
        self.resolution = game_context.resolution
        self.game_context = game_context
        self.sprite_groups = dict()

    def load_graphics(self):
        self.spriteslib = SpritesLib(self.game_context)
        self.spriteslib.add_sheet("main", os.path.normpath("assets/spritelib_gpl/shooter/disasteroids2_master.png"), (0, 0, 0))
        self.spriteslib.add_sheet("explode3", os.path.normpath("assets/spritesheets/Explode3.bmp"), (69, 78, 91))
        self.game_context.add("sprites", self.spriteslib)

    def load_sounds(self):
        self.soundslib = SoundsLib()
        self.soundslib.add_sound("alloyshipthrust", os.path.normpath("assets/sounds/alloyshipthrust.wav"))
        self.soundslib.add_sound("gunshot", os.path.normpath("assets/sounds/gunshot.wav"))
        self.soundslib.add_sound("gunblast", os.path.normpath("assets/sounds/gunblast.wav"))
        self.game_context.add("sounds", self.soundslib)

    def load_music(self):
        pass

    def load_fonts(self):
        self.textlib = TextLib(self.spriteslib)
        self.game_context.add("text", self.textlib)

    def load_maps(self):
        # load map file
        ranges = {}
        ranges['interval_min'] = 10
        ranges['interval_max'] = 10
        ranges['count_min'] = 3
        ranges['count_max'] = 5
        ranges['direction_min'] = 0
        ranges['direction_max'] = 360
        ranges['speed_min'] = 30
        ranges['speed_max'] = 70
        ranges['position_type'] = "offmap"
        starting_room = RoomMap(self.game_context, "start", (32, 32), (30, 30), None)

        # Mobs
        #initdata = starting_room.generate_random_init(ranges)
        # asteroids
        initdata = starting_room.generate_random_init(ranges)
        starting_room.add_mob(Asteroid, initdata)
        starting_room.add_spawns(Asteroid, ranges=ranges)
        # ufo
        initdata = starting_room.generate_random_init(ranges)
        initdata['targets'] = [self.players["player_one"].main_sprite]
        starting_room.add_mob(Ufo, initdata=initdata)
        # staring_room.loadtiles()
        # turret
        initdata = starting_room.generate_random_init(ranges)
        ranges['position_type'] = "inmap"
        initdata['targets'] = [self.players["player_one"].main_sprite]
        starting_room.add_mob(Turret, initdata)


        self.worldmap.add_room(starting_room, (0, 0))

    def init_controls(self, controls_config):
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_LEFT,  self.players["player_one"].main_sprite.rotate_left)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_LEFT,  self.players["player_one"].main_sprite.stop_rotate_left)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_RIGHT,  self.players["player_one"].main_sprite.rotate_right)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_RIGHT,  self.players["player_one"].main_sprite.stop_rotate_right)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_UP,  self.players["player_one"].keypress_up)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_UP,  self.players["player_one"].keyrelease_up)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_SPACE,  self.players["player_one"].shoot)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_SPACE,  self.players["player_one"].stop_shooting)

    def initgame(self):
        self.load_sounds()
        self.load_graphics()
        self.load_music()
        self.load_fonts()
        initdata = {}
        initdata['centerx'] = 600
        initdata['centery'] = 400
        self.players["player_one"] = Player(AlloyShip, self.game_context, initdata=initdata)
        self.load_maps()
        self.init_controls(None)

    def initlevel(self, levelid):
        self.elements.empty()
        self.worldmap.set_current_room((0, 0))

    def initcutscene(self, cutsceneid):
        pass

    def collisions(self):
        for sprite in self.elements.sprites():
            # if sprite is in element, collide return as if sprite collides with itself
            if not sprite.immutable and not sprite.full_screen:
                self.elements.remove(sprite)
                sprite.active_collisions.empty()
                collided = pygame.sprite.spritecollide(sprite, self.elements, False, collided=pygame.sprite.collide_rect)
                for collided_sprite in collided:
                    if not collided_sprite.full_screen:
                        point = pygame.sprite.collide_mask(sprite, collided_sprite)
                        if point:
                            sprite.active_collisions.add(collided_sprite)
                            sprite.collision_points[collided_sprite] = point
                    else:
                        y = collided_sprite.m * sprite.rect.x + collided_sprite.q
                        if y > sprite.rect.y and y < sprite.rect.y + sprite.rect.height:
                                point = pygame.sprite.collide_mask(sprite, collided_sprite)
                                if point:
                                    sprite.active_collisions.add(collided_sprite)
                                    sprite.collision_points[collided_sprite] = point
                self.elements.add(sprite)

    def update_level(self):
        self.worldmap.get_current_room().update()
        room_elements = self.worldmap.get_current_room().elements
        self.elements.add(room_elements.sprites(), layer=1)
        self.elements.remove_sprites_of_layer(3)
        player_one = self.players["player_one"].main_sprite
        for player in self.players.values():
            self.elements.add(player.sprites(), layer=2)

    def update(self):
        self.elements.empty()
        if self.status == "start":
            self.initlevel("startlevel")
            self.status = "level"
        if self.status == "level":
            self.update_level()
        self.collisions()
        for sprite in self.elements.sprites():
            if getattr(sprite, "destroyed", False):
                sprite.kill()
                del (sprite)
        self.elements.update()
        return False, None, self.elements
