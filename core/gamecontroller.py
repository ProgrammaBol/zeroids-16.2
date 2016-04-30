import pygame
import pprint
from maps import RoomMap, WorldMap
from asteroids import Asteroid
from players import Player, AlloyShip
from ufo import Ufo
from turret import Turret
# levels (roomid)

def weightedcollide():
    pass


class GameController(object):

    def __init__(self, event_queue, game_context):
        self.players = dict()
        self.status = "menu-init"
        self.worldmap = WorldMap((1, 4))
        self.elements = pygame.sprite.LayeredUpdates()
        self.event_queue = event_queue
        self.clock = game_context.clock
        self.resolution = game_context.resolution
        self.game_context = game_context
        self.sprite_groups = dict()
        self.pause = False
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_p, self.toggle_pause)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_n, self.next_level)
        self.currentstatus_elements = dict()

    def next_level(self):
        self.status = "level-init"

    def load_map(self, levelid):
        # load map file(levelid)
        if levelid == (0,0):
            map_def = {
                'name' : 'Level 1',
                'size' : (32, 32),
                'tilesize' : (30,30),
                'tilemap' : None,
                'player_pos' : (600,400),
                'random_ranges' : {
                    'interval_min' : 10,
                    'interval_max' : 10,
                    'count_min' : 3,
                    'count_max' : 5,
                    'direction_min' : 0,
                    'direction_max' : 360,
                    'speed_min' : 30,
                    'speed_max' : 70,
                    'position_type' : "offmap",
                },
                'mobs': [],
                'spawns': []
            }
        if levelid == (0,1):
            map_def = {
                'name' : 'Level 2',
                'size' : (32, 32),
                'tilesize' : (30,30),
                'tilemap' : None,
                'player_pos' : (600,400),
                'random_ranges' : {
                    'interval_min' : 10,
                    'interval_max' : 10,
                    'count_min' : 3,
                    'count_max' : 5,
                    'direction_min' : 0,
                    'direction_max' : 360,
                    'speed_min' : 30,
                    'speed_max' : 70,
                    'position_type' : "offmap",
                },
                'mobs': [
                    ('Asteroid', None)
                ],
                'spawns': []
            }
        room = RoomMap(self.game_context, map_def)

        # Mobs
        #room.add_spawns(Asteroid, randome_ranges=random_ranges)
        # ufo
        #initdata = {}
        #initdata['targets'] = [self.players["player_one"].main_sprite]
        #room.add_mob(Ufo, initdata=initdata, random_ranges=random_ranges)
        # staring_room.loadtiles()
        # turret
        #random_ranges['position_type'] = "inmap"
        #initdata['targets'] = [self.players["player_one"].main_sprite]
        #room.add_mob(Turret, initdata=initdata, random_ranges=random_ranges)

        self.worldmap.add_room(room, levelid)

    def toggle_pause(self):
        self.pause = not self.pause

    def init_controls(self, controls_config):
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_LEFT,  self.players["player_one"].main_sprite.rotate_left)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_LEFT,  self.players["player_one"].main_sprite.stop_rotate_left)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_RIGHT,  self.players["player_one"].main_sprite.rotate_right)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_RIGHT,  self.players["player_one"].main_sprite.stop_rotate_right)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_UP,  self.players["player_one"].keypress_up)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_UP,  self.players["player_one"].keyrelease_up)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_SPACE,  self.players["player_one"].shoot)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_SPACE,  self.players["player_one"].stop_shooting)

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
                    if not collided_sprite.full_screen and not collided_sprite.immutable:
                        point = pygame.sprite.collide_mask(sprite, collided_sprite)
                        if point:
                            sprite.active_collisions.add(collided_sprite)
                            sprite.collision_points[collided_sprite] = point
                    elif collided_sprite.full_screen:
                        y = collided_sprite.m * sprite.rect.x + collided_sprite.q
                        if y > sprite.rect.y and y < sprite.rect.y + sprite.rect.height:
                                point = pygame.sprite.collide_mask(sprite, collided_sprite)
                                if point:
                                    sprite.active_collisions.add(collided_sprite)
                                    sprite.collision_points[collided_sprite] = point
                self.elements.add(sprite)

    def change_status(self, status):
        self.status = status

    def gameover(self):
        self.status = "menu-init"

    def menu_shutdown(self):
        self.event_queue.unsubscribe("keyboard", pygame.KEYUP, pygame.K_SPACE)
        self.currentstatus_elements['startbutton'].destroyed = True

    def menu_startgame(self):
        self.menu_shutdown()
        self.status = "level-init"

    def menu_init(self):
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_SPACE, self.menu_startgame)
        text = "Press space to start"
        self.currentstatus_elements['startbutton'] = self.game_context.text.get_textsprite(text, style="title")

    def menu_update(self):
        self.elements.add(self.currentstatus_elements['startbutton'])

    def intralevel_init(self, room):
        text = room.name
        self.currentstatus_elements['levelname'] = self.game_context.text.get_textsprite(text, style="title")
        self.status = "intralevel"
        self.countdown = 2000

    def intralevel_update(self, room):
        self.countdown = self.countdown - self.clock.get_time()
        if self.countdown <= 0:
            self.status = "level"
            self.currentstatus_elements['levelname'].destroyed = True
        else:
            self.elements.add(self.currentstatus_elements['levelname'])


    def level_init(self, levelid=(0,0)):
        self.load_map(levelid)
        player_initdata = self.worldmap.set_current_room(levelid)
        self.players["player_one"] = Player(AlloyShip, self.game_context, initdata=player_initdata)
        self.init_controls(None)

    def level_update(self, room):
        room_elements, mobs = room.update()
        self.elements.add(room_elements.sprites(), layer=1)
        self.elements.remove_sprites_of_layer(3)
        for mob in mobs:
            self.elements.add(mob.sprites())
        for player in self.players.values():
            self.elements.add(player.sprites(), layer=2)
        self.collisions()

        # player on health = 0
        # self.status = game over
        # if level_completed
        # self.status = "leve_init"

    def update(self):
        if self.pause:
            return False, None, self.elements
        self.elements.empty()
        # Statuses
        if self.status == "game-over":
            self.gameover()
        if self.status == "menu-init":
            self.menu_init()
            self.status = "menu"
        if self.status == "menu":
            self.menu_update()
        if self.status == "level-init":
            levelid = self.worldmap.get_current_room_id()
            if levelid is None:
                next_levelid = (0,0)
            else:
                next_levelid = (0, levelid[1] + 1)
            self.level_init(next_levelid)
            self.status = "intralevel-init"
        if self.status == "intralevel-init":
            room = self.worldmap.get_current_room()
            self.intralevel_init(room)
        if self.status == "intralevel":
            room = self.worldmap.get_current_room()
            self.intralevel_update(room)
        if self.status == "level":
            room = self.worldmap.get_current_room()
            self.level_update(room)

        for sprite in self.elements.sprites():
            if getattr(sprite, "destroyed", False):
                sprite.kill()
                del (sprite)

        self.elements.update()

        return False, None, self.elements
