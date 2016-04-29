from exceptions import AnimationEnded

class Animation(object):

    def __init__(self, game_context, sprite, name):
        self.name = name
        self.sprite = sprite
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
        costume_name = "animation-%s-%s" % (self.name, self.playback_position)
        self.sprite.change_active_costume(costume_name)
        time_msec = self.clock.get_time()
        self.nextframe_countdown -= time_msec
        if self.nextframe_countdown <= 0:
            self.playback_position += 1
            if self.playback_position > len(self.sequence) - 1:
                raise AnimationEnded
            self.nextframe_countdown = self.sequence[costume_name]
