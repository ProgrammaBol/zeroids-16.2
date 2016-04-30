import pygame
'''
        text = unicode("speed_x: %s, speed_y: %s" % (player_one.speed_x, player_one.speed_y))
        textsprite = self.textlib.get_textsprite(text)
        self.elements.add(textsprite, layer=3)
'''
class TextLib(object):

    def __init__(self, game_context):
        self.styles = dict()
        self.game_context = game_context
        fontname = pygame.font.get_default_font()
        self.styles['default'] = dict()
        self.styles['default']['font'] = pygame.font.SysFont(fontname, 20)
        self.styles['default']['position'] = "top"
        self.styles['title'] = dict()
        self.styles['title']['font'] = pygame.font.SysFont(fontname, 100)
        self.styles['title']['position'] = "center"
        self.styles['status'] = dict()
        self.styles['status']['font'] = pygame.font.SysFont(fontname, 20)
        self.styles['status']['position'] = "bottom"


    def get_textsprite(self, text, style="default", color=(255,255,255)):
        textimage = self.styles[style]['font'].render(text, True, color)
        textsprite = pygame.sprite.Sprite()
        textsprite.image = textimage
        textsprite.immutable = True
        textsprite.rect = textimage.get_rect()
        if self.styles[style]['position'] == "center":
            textsprite.rect.centerx = self.game_context.resolution[0]/2
            textsprite.rect.centery = self.game_context.resolution[1]/2
        if self.styles[style]['position'] == "top":
            pass
        if self.styles[style]['position'] == "bottom":
            self.rect.y = self.game_context.resolution[1] - self.rect.height

        return textsprite
