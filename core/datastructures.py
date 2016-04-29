import pygame

class GameContext(object):

    def __init__(self, context):
        for k,v in context.iteritems():
            setattr(self, k, v)

    def add(self, key, value):
        setattr(self, key, value)

class EventQueue(object):

    def __init__(self):
        self.subscriptions = dict()
        self.subscriptions["keyboard"] = dict()

    def subscribe(self, eventsource, eventtype, eventid, callback_handler):
        if eventtype not in self.subscriptions[eventsource]:
            self.subscriptions[eventsource][eventtype] = dict()
        self.subscriptions[eventsource][eventtype][eventid] = callback_handler

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for eventtype in self.subscriptions["keyboard"]:
                if event.type == eventtype:
                    for eventid in self.subscriptions["keyboard"][eventtype]:
                        if event.key == eventid:
                            handler = self.subscriptions["keyboard"][eventtype][eventid]
                            handler()
        return True
