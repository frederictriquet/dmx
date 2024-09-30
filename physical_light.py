import time

class PhysicalLight:
    def __init__(self, name: str, channel: int, fixture: dict, dmx):
        self.name = name
        self.channel = channel
        self.fixture = fixture
        self.previous_color = (0,0,0,0,0)
        self.current_color = (0,0,0,0,0)
        self.next_color = (0,0,0,0,0)
        self.t0 = None
        self.fade_time = 0.0
        self.dimmer = 0
        self.strobe = 0
        self.dmx = dmx
        if 'class' in fixture:
            import importlib
            module = importlib.import_module(fixture['class']['module_name'])
            class_obj = getattr(module, fixture['class']['class_name'])
            self.light_object = class_obj(self)
        else:
            self.light_object = None

    def __repr__(self):
        return f'{self.name}: {self.channel} {self.fixture}\n'

    def set_next_color(self, color_code: str, fade_time: float):
        self.t0 = time.time()
        self.fade_time = fade_time
        self.previous_color = self.current_color
        r = int(color_code[0:2], 16)
        g = int(color_code[2:4], 16)
        b = int(color_code[4:6], 16)
        w = int(color_code[6:8], 16)
        a = int(color_code[8:10], 16)
        self.next_color = (r,g,b,w,a)

    def set_dimmer(self, dimmer: int):
        self.dimmer = dimmer

    def set_strobe(self, strobe: int):
        self.strobe = strobe

    def tick(self):
        if self.t0:
            interval = time.time() - self.t0
            if interval > self.fade_time or self.fade_time == 0:
                delta = 1
                self.t0 = None
            else:
                delta = interval/self.fade_time
            self.current_color = tuple(int(self.previous_color[i]*(1.0-delta) + self.next_color[i]*delta) for i in range(0,5))
        self.set_full()

    def set_full(self):
        if self.light_object:
            self.light_object.set_full()
            return
        mode = 'color' if self.strobe==0 else 'strobe'
        for index, c in enumerate(self.fixture['channels'][mode]):
            if c == 'dimmer':
                self.dmx.set_channel(self.channel+index, self.dimmer)
            elif c == 'red':
                self.dmx.set_channel(self.channel+index, self.current_color[0])
            elif c == 'green':
                self.dmx.set_channel(self.channel+index, self.current_color[1])
            elif c == 'blue':
                self.dmx.set_channel(self.channel+index, self.current_color[2])
            elif c == 'white':
                self.dmx.set_channel(self.channel+index, self.current_color[3])
            elif c == 'amber':
                self.dmx.set_channel(self.channel+index, self.current_color[4])
            elif c == 'strobe':
                self.dmx.set_channel(self.channel+index, self.strobe)
            elif isinstance(c, int):
                self.dmx.set_channel(self.channel+index, c)
