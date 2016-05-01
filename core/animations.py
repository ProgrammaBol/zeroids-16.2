from exceptions import AnimationEnded

class Animation(object):

    def __init__(self, game_context, sprite, name, sound=None):
        self.name = name
        self.sprite = sprite
        self.sound = sound
        self.sequence = {}
        self.playback_position = 0
        self.clock = game_context.clock
        self.nextframe_countdown = 0

    def add_sequence(self, sequence, total_duration, equal_time=False, defs=True):
        # TYPE can be costumes or blitover
        for frame in sequence:
            if equal_time:
                frame_image = frame
                frame_duration = total_duration/len(sequence)
            else:
                frame_image = frame[0]
                frame_duration = frame[1]
            self.add_frame(frame_image, duration_msec=frame_duration, defs=defs)

    def add_frame(self, frame, duration_msec=0, defs=True):
        count = len(self.sequence)
        if count == 1:
            self.nextframe_countdown = duration_msec
        costume_name = "animation-%s-%s" % (self.name, count)
        if defs:
            self.sprite.costumes_defs[costume_name] = frame
        else:
            self.sprite.costumes[costume_name] = frame
        self.sequence[costume_name] = duration_msec

    def update(self):
        if self.playback_position == 0 and self.sound is not None:
            # play sound
            pass
        costume_name = "animation-%s-%s" % (self.name, self.playback_position)
        self.sprite.change_active_costume(costume_name)
        time_msec = self.clock.get_time()
        self.nextframe_countdown -= time_msec
        if self.nextframe_countdown <= 0:
            self.playback_position += 1
            if self.playback_position > len(self.sequence) - 1:
                raise AnimationEnded
            self.nextframe_countdown = self.sequence[costume_name]

class Animations(object):

    def __init__(self, game_context):
        self.game_context = game_context
        self.animations = {}
        self.animations['explode'] = {}
        self.animations['explode'][3] = {}
        self.animations['explode'][3]['sound'] = None
        self.animations['explode'][3]['duration'] = 1000
        self.animations['explode'][3]['equal-time'] = True
        self.animations['explode'][3]['seq'] = [
            ("explode3", (0, 0, 47, 47)),
            ("explode3", (49, 0, 47, 47)),
            ("explode3", (97, 0, 47, 47)),
            ("explode3", (145, 0, 47, 47)),
            ("explode3", (0, 49, 47, 47)),
            ("explode3", (49, 49, 47, 47)),
            ("explode3", (97, 49, 47, 47)),
            ("explode3", (145, 49, 47, 47)),
        ]
        self.animations['explode'][2] = {}
        self.animations['explode'][2]['sound'] = None
        self.animations['explode'][2]['duration'] = 1000
        self.animations['explode'][2]['equal-time'] = True
        self.animations['explode'][2]['seq'] = [
            ("explode2", (1, 1, 22, 22)),
            ("explode2", (25, 1, 22, 22)),
            ("explode2", (49, 1, 22, 22)),
            ("explode2", (73, 1, 22, 22)),
            ("explode2", (97, 1, 22, 22)),
            ("explode2", (121, 1, 22, 22)),
            ("explode2", (145, 1, 22, 22)),
            ("explode2", (169, 1, 22, 22)),
        ]
        self.animations['explode'][1] = {}
        self.animations['explode'][1]['sound'] = None
        self.animations['explode'][1]['duration'] = 1000
        self.animations['explode'][1]['equal-time'] = True
        self.animations['explode'][1]['seq'] = [
            ("explode1", (1, 1, 10, 10)),
            ("explode1", (13, 1, 10, 10)),
            ("explode1", (25, 1, 10, 10)),
            ("explode1", (37, 1, 10, 10)),
            ("explode1", (49, 1, 10, 10)),
            ("explode1", (61, 1, 10, 10)),
            ("explode1", (73, 1, 10, 10)),
        ]

    def get_animation(self, sprite, name, size):
        animation = Animation(self.game_context, sprite, name, sound = self.animations['explode'][1]['sound'])
        animation.add_sequence(self.animations[name][size]['seq'],
                               self.animations['explode'][1]['duration'],
                               equal_time=self.animations['explode'][1]['equal-time'],
                               defs=True)
        return animation
