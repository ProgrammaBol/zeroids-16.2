import pygame
import pprint
from maps import RoomMap, WorldMap
# levels (roomid)

def weightedcollide():
    pass


class GameController(object):

    def __init__(self, event_queue, game_context):
        self.players = dict()
        self.status = "menu-init"
        self.worldmap = WorldMap(game_context, (1, 5))
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

    def toggle_pause(self):
        self.pause = not self.pause

    def init_controls(self, controls_config):
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_LEFT,  self.players["player_one"].keypress_left)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_LEFT,  self.players["player_one"].keyrelease_left)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_RIGHT,  self.players["player_one"].keypress_right)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_RIGHT,  self.players["player_one"].keyrelease_right)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_UP,  self.players["player_one"].keypress_up)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_UP,  self.players["player_one"].keyrelease_up)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_DOWN,  self.players["player_one"].keyrelease_down)
        self.event_queue.subscribe("keyboard", pygame.KEYDOWN, pygame.K_SPACE,  self.players["player_one"].keypress_space)
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_SPACE,  self.players["player_one"].keyrelease_space)

    def initcutscene(self, cutsceneid):
        pass

    def collisions(self):
        collision_elements = self.elements.copy()
        collision_pairs = []
        for sprite in collision_elements:
            if not sprite.immutable:
                sprite.active_collisions.empty()
        while collision_elements.sprites():
            sprite = collision_elements.sprites().pop(0)
            collision_elements.remove(sprite)
            collided = pygame.sprite.spritecollide(sprite, collision_elements, False)
            if not collided:
                continue
            for collided_sprite in collided:
                pair = set([sprite, collided_sprite])
                if pair in collision_pairs:
                    continue
                else:
                    collision_pairs.append(pair)
                point = None
                if collided_sprite.shape != "line" and sprite.shape != "line":
                    point = pygame.sprite.collide_mask(sprite, collided_sprite)
                elif collided_sprite.shape == "line" and sprite.shape != "line":
                    y = collided_sprite.m * sprite.centerx + collided_sprite.q
                    if y >= sprite.rect.y and y <= sprite.rect.y + sprite.rect.height:
                        point = pygame.sprite.collide_mask(sprite, collided_sprite)
                elif collided_sprite.shape != "line" and sprite.shape == "line":
                    y = sprite.m * collided_sprite.centerx + sprite.q
                    if y >= collided_sprite.rect.y and y <= collided_sprite.rect.y + collided_sprite.rect.height:
                        point = pygame.sprite.collide_mask(sprite, collided_sprite)
                if point:
                    if not sprite.immutable:
                        sprite.active_collisions.add(collided_sprite)
                        sprite.collision_points[collided_sprite] = point
                    if not collided_sprite.immutable:
                        point = pygame.sprite.collide_mask(collided_sprite, sprite)
                        collided_sprite.active_collisions.add(sprite)
                        collided_sprite.collision_points[sprite] = point


    def change_status(self, status):
        self.status = status

    def gameover(self):
        self.status = "menu-init"

    def menu_shutdown(self):
        self.event_queue.unsubscribe("keyboard", pygame.KEYUP, pygame.K_SPACE)
        self.currentstatus_elements['startbutton'].destroyed = True
        self.currentstatus_elements['title'].destroyed = True

    def menu_startgame(self):
        self.menu_shutdown()
        self.status = "level-init"

    def menu_init(self):
        self.event_queue.subscribe("keyboard", pygame.KEYUP, pygame.K_SPACE, self.menu_startgame)
        text = "Press space to start"
        self.currentstatus_elements['startbutton'] = self.game_context.text.get_textsprite(text, style="subtitle")
        titletext = "Zeroids"
        self.currentstatus_elements['title'] = self.game_context.text.get_textsprite(titletext, style="title", color=(255,100,0))

    def menu_update(self):
        self.elements.add(self.currentstatus_elements['startbutton'])
        self.elements.add(self.currentstatus_elements['title'])

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
        self.players = self.worldmap.load_room(levelid)
        self.init_controls(None)
        text = "HEALTH: %d" % self.players['player_one'].health
        self.currentstatus_elements['health'] = self.game_context.text.get_textsprite(text)

    def level_update(self, room):
        room_elements, mobs = room.update()
        self.elements.add(room_elements.sprites(), layer=1)
        self.elements.remove_sprites_of_layer(3)
        text = "HEALTH: %d" % self.players['player_one'].health
        self.currentstatus_elements['health'].set_text(text)
        self.elements.add(self.currentstatus_elements['health'])
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

        self.elements.update()

        return False, None, self.elements
