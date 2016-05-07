import pygame
import os
'''
text = unicode("speed_x: %s, speed_y: %s" % (player_one.speed_x, player_one.speed_y))
textsprite = self.textlib.get_textsprite(text)
self.elements.add(textsprite, layer=3)
'''


class TextSprite(pygame.sprite.Sprite):

    def __init__(self, game_context, text, font, position, color, *group):
        super(TextSprite, self).__init__(*group)
        self.font = font
        self.text = text
        self.position = position
        self.game_context = game_context
        self.collision_entity = "text"
        self.color = color
        self.set_text(self.text, color=color)
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.shape = "text"
        self.immutable = True
        self.parent = None

    def set_text(self, text, color=(255, 255, 255)):
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        if self.position == "center":
            self.rect.centerx = self.game_context.resolution[0]/2
            self.rect.centery = self.game_context.resolution[1]/2
        if self.position == "top":
            pass
        if self.position == "bottom":
            self.rect.y = self.game_context.resolution[1] - self.rect.height
        if self.position == "top-center":
            self.rect.centerx = self.game_context.resolution[0]/2
            self.rect.centery = self.game_context.resolution[1]/2 - 200
        if self.position == "bottom-center":
            self.rect.centerx = self.game_context.resolution[0]/2
            self.rect.centery = self.game_context.resolution[1]/2 + 200



class TextLib(object):

    def __init__(self, game_context):
        self.styles = dict()
        self.game_context = game_context
        fontname = pygame.font.get_default_font()
        titlefont = os.path.normpath("assets/font/Dosis-ExtraBold.otf")
        self.styles['default'] = dict()
        self.styles['default']['font'] = pygame.font.SysFont(fontname, 20)
        self.styles['default']['position'] = "top"
        self.styles['subtitle'] = dict()
        self.styles['subtitle']['font'] = pygame.font.SysFont(fontname, 100)
        self.styles['subtitle']['position'] = "bottom-center"
        self.styles['status'] = dict()
        self.styles['status']['font'] = pygame.font.SysFont(fontname, 20)
        self.styles['status']['position'] = "bottom"
        self.styles['title'] = dict()
        self.styles['title']['font'] = pygame.font.Font(titlefont, 170)
        self.styles['title']['position'] = "top-center"

    def get_textsprite(self, text, style="default", color=(255,255,255)):
        textsprite = TextSprite(self.game_context, text, self.styles[style]['font'], self.styles[style]['position'], color)
        return textsprite
