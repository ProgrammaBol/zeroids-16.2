import pygame


class SoundsLib(object):

    def __init__(self):
        pygame.mixer.stop()
        pygame.mixer.set_num_channels(32)
        pygame.mixer.set_reserved(4)
        self.sounds = dict()
        self.musics = dict()
        self.channels = dict()

    def add_sound(self, name, filename, volume=None):
        self.sounds[name] = pygame.mixer.Sound(filename)

    def add_music(self, name, filename, volume=None):
        self.sounds[name] = filename

    def loop_play(self, name):
        channel = pygame.mixer.find_channel(True)
        self.channels[id(channel)] = channel
        self.channels[id(channel)].play(self.sounds[name], loops=-1)
        return id(channel)

    def stop_loop(self, channelid):
        self.channels[channelid].stop()
        del (self.channels[channelid])

    def single_play(self, name):
        channel = pygame.mixer.find_channel(True)
        channel.play(self.sounds[name])

    def music_play(self, name):
        filename = self.music[name]
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
