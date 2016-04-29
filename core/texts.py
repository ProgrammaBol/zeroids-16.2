import pygame
'''
        text = unicode("speed_x: %s, speed_y: %s" % (player_one.speed_x, player_one.speed_y))
        textsprite = self.textlib.get_textsprite(text)
        self.elements.add(textsprite, layer=3)
'''
class TextLib(object):

    def __init__(self, spriteslib):
        self.styles = dict()
        self.spriteslib = spriteslib
        fontname = pygame.font.get_default_font()
        self.styles['default'] = pygame.font.SysFont(fontname, 20)

    def get_textsprite(self, text, style="default", color=(255,255,255)):
        textimage = self.styles[style].render(text, True, color)
        textsprite = pygame.sprite.Sprite()
        textsprite.image = textimage
        textsprite.immutable = True
        textsprite.rect = textimage.get_rect()
        textsprite.active_collisions = pygame.sprite.GroupSingle()
        textsprite.collision_entity = "text"
        return textsprite
