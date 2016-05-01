import pygame
import random
from sprites import StaticSprite
from asteroids import Asteroid

class TileSet(dict):

    def __init__(self):
        pass


class Tile(StaticSprite):

    def __init__(self, tilemap, *group):
        self.tilemap = tilemap
        self.destructable = False
        super(Tile, self).__init__(*group)

        (spritesheet_name, rect) = tilemap[tileid]
        tile = StaticSprite(spritesheet_name, rect)


class Background(object):

    def __init__(self, color, image=None):
        self.color = color
        self.image = image

    def draw(self, screensize):
        surface = pygame.Surface(screensize)
        surface.fill(self.color)
        if self.image is not None:
            pass
        return (surface, (0, 0))


class RoomMap(object):

    def __init__(self, game_context, map_def):
        self.name = map_def['name']
        self.elements = pygame.sprite.Group()
        size = map_def['size']
        self.tiles = list([None for r in range(size[1])] for c in range(size[0]))
        self.background = Background((0, 0, 0))
        self.tilesize = map_def['tilesize']
        self.tilemap = map_def['tilemap']
        self.mobs = []
        self.spawns = {}
        self.clock = game_context.clock
        self.resolution = game_context.resolution
        self.game_context = game_context
        self.player_pos = map_def['player_pos']
        spawns = map_def.get('spawns', [])
        for spawn_group in spawns:
            mob_class_name, definitions = spawn_group.popitem()
            self.add_spawns(mob_class_name, definitions)



    def load_map_def(self, map_def):
        pass

    def generate_random_init(self, ranges):
        pass

    def set_tile(self, tileid, position):
        tile = self.tiles[position[0]][position[1]]
        if tile:
            self.elements.remove(tile)
            del(tile)
        tile = Tile(tileid)
        tile.set_position(position[0] * self.tilesize[0], position[1] * self.tilesize[1])
        self.tiles[position[0]][position[1]] = tile
        self.elements.add(tile)

    def load_tile_positions(self, tile_positions):
        for tileid, position in tile_positions:
            self.set_tile(tileid, position)

    def set_background(self, color, image=None):
        self.background.color = color
        self.background.image = image

    def add_mob(self, mob_class, initdata={}, random_ranges=None):
        #sprite = mob.main_sprite
        #sprite.centerx = position[0] * self.tilesize[0] + self.tilesize[0]/2
        #sprite.centery = position[1] * self.tilesize[1] + self.tilesize[1]/2
        #sprite.setup_ai(ai_scheme)
        return mob

    def add_spawn(self, mob_class, inidata=None, random_ranges=None):
        pass

    def add_spawns(self, mob_class_name, definitions):
        initdata = definitions.get('initdata', {})
        random_ranges = definitions.get('random_ranges', None)
        multiple = definitions.get('multiple', True)
        ''' if mutiple=False a new spawn will not be created if the first
        is still present '''
        if not initdata and random_ranges is None:
            raise Exception
        try:
            mob_class = globals()[mob_class_name]
        except KeyError:
            return None


        self.spawns[mob_class.__name__] = {}
        count_min = random_ranges.get('count_min', 1)
        count_max = random_ranges.get('count_max', 1)
        count = random.randint(count_min, count_max)
        intervals = []
        for spawn in range(count):
            interval_min = float(random_ranges.get('interval_min', 0.0))
            interval_max = float(random_ranges.get('interval_max', 0.0))
            interval = random.randint(interval_min, interval_max)
            intervals.append(interval)

        self.spawns[mob_class.__name__]['completed'] = False
        self.spawns[mob_class.__name__]['class'] = mob_class
        self.spawns[mob_class.__name__]['initdata'] = initdata
        self.spawns[mob_class.__name__]['random_ranges'] = random_ranges
        self.spawns[mob_class.__name__]['last'] = None
        self.spawns[mob_class.__name__]['multiple'] = multiple
        self.spawns[mob_class.__name__]['intervals'] = intervals
        self.spawns[mob_class.__name__]['next_countdown'] = intervals.pop(0)

    def update(self):
        for mob_class, infos in self.spawns.iteritems():
            if infos['completed']:
                continue
            time = float(self.clock.get_time())/1000.0
            infos['next_countdown'] -= time
            random_ranges = infos['random_ranges']
            if infos['next_countdown'] <= 0:
                initdata = infos['initdata']
                mob_class = infos['class']
                mob = mob_class(self.game_context, initdata=initdata, random_ranges=random_ranges)
                self.mobs.append(mob)
                infos['last'] = mob
                try:
                    infos['next_countdown'] = infos['intervals'].pop(0)
                except IndexError:
                    infos['completed'] = True

        return self.elements, self.mobs

class WorldMap(object):

    def __init__(self, size):
        self.rooms = list([None for r in range(size[1])] for c in range(size[0]))
        self.current_room = None
        self.size = size

    def add_room(self, room_map, position):
        self.rooms[position[0]][position[1]] = room_map

    def set_current_room(self, position):
        north = None
        south = None
        east = None
        west = None
        if position[1] != 0:
            north = self.rooms[position[0]][position[1] + 1]
        if position[1] != self.size[1] - 1:
            south = self.rooms[position[0]][position[1] - 1]
        if position[0] != 0:
            east = self.rooms[position[0] + 1][position[1]]
        if position[0] != self.size[0] - 1:
            west = self.rooms[position[0] - 1][position[1]]

        self.current_exits = (north, south, east, west)
        self.current_room = position
        room = self.rooms[self.current_room[0]][self.current_room[1]]

        player_initdata = dict()
        player_initdata['centerx'] = room.player_pos[0]
        player_initdata['centery'] = room.player_pos[1]

        return player_initdata

    def get_current_room(self):
        return self.rooms[self.current_room[0]][self.current_room[1]]

    def get_current_room_id(self):
        if self.current_room is None:
            return None
        return (self.current_room[0],self.current_room[1])
