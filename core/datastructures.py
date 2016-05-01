import pygame
import os
from sprites import SpritesLib
from sounds import SoundsLib
from texts import TextLib
from animations import Animations

class GameContext(object):

    def __init__(self, context):
        for k,v in context.iteritems():
            setattr(self, k, v)
        self.load_sounds()
        self.load_graphics()
        self.load_music()
        self.load_fonts()
        self.load_animations()

    def add(self, key, value):
        setattr(self, key, value)

    def load_graphics(self):
        self.spriteslib = SpritesLib(self)
        self.spriteslib.add_sheet("main", os.path.normpath("assets/spritesheets/master.png"), (0, 0, 0))
        self.spriteslib.add_sheet("extended", os.path.normpath("assets/spritesheets/extended.png"), (171, 166, 166))
        self.spriteslib.add_sheet("explode3", os.path.normpath("assets/spritesheets/Explode3.bmp"), (69, 78, 91))
        self.spriteslib.add_sheet("explode2", os.path.normpath("assets/spritesheets/Explode1.bmp"), (0, 0, 0))
        self.spriteslib.add_sheet("explode1", os.path.normpath("assets/spritesheets/Explode2.bmp"), (0, 0, 0))
        self.add("sprites", self.spriteslib)

    def load_sounds(self):
        self.soundslib = SoundsLib()
        self.soundslib.add_sound("alloyshipthrust", os.path.normpath("assets/sounds/alloyshipthrust.wav"))
        self.soundslib.add_sound("gunshot", os.path.normpath("assets/sounds/gunshot.wav"))
        self.soundslib.add_sound("gunblast", os.path.normpath("assets/sounds/gunblast.wav"))
        self.soundslib.add_sound("explosion", os.path.normpath("assets/sounds/explosion.wav"))
        self.add("sounds", self.soundslib)

    def load_music(self):
        self.soundslib.add_music("intro", os.path.normpath("assets/music/intro.wav"))

    def load_animations(self):
        self.animations = Animations(self)

    def load_fonts(self):
        self.textlib = TextLib(self)
        self.add("text", self.textlib)

class EventQueue(object):

    def __init__(self):
        self.subscriptions = dict()
        self.subscriptions["keyboard"] = dict()

    def subscribe(self, eventsource, eventtype, eventid, callback_handler):
        if eventtype not in self.subscriptions[eventsource]:
            self.subscriptions[eventsource][eventtype] = dict()
        self.subscriptions[eventsource][eventtype][eventid] = callback_handler

    def unsubscribe(self, eventsource, eventtype, eventid):
        if eventsource in self.subscriptions and eventtype in self.subscriptions[eventsource] and eventid in self.subscriptions[eventsource][eventtype]:
            self.subscriptions[eventsource][eventtype][eventid]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for eventtype in self.subscriptions["keyboard"]:
                if event.type == eventtype:
                    for eventid in self.subscriptions["keyboard"][eventtype]:
                        if event.key == eventid:
                            handler = self.subscriptions["keyboard"][eventtype][eventid]
                            if handler is not None:
                                handler()
        return True
