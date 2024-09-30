from physical_light import PhysicalLight

class IrLED64:
    def __init__(self, physical_light: PhysicalLight):
        self.physical_light = physical_light

    def set_full(self):
        l = self.physical_light
        dmx_chan = l.channel
        l.dmx.set_channel(dmx_chan+0, l.current_color[0]) # r
        l.dmx.set_channel(dmx_chan+1, l.current_color[1]) # g
        l.dmx.set_channel(dmx_chan+2, l.current_color[2]) # b
        l.dmx.set_channel(dmx_chan+3, l.current_color[3]) # w
        l.dmx.set_channel(dmx_chan+4, l.current_color[4]) # a
        if l.strobe == 0:
            # 0->189
            dimmer_value = int(l.dimmer*189/255)
            l.dmx.set_channel(dmx_chan+5, dimmer_value) # dimmer
        else:
            # 190->250
            strobe_value = int(l.strobe*60/255 + 190)
            l.dmx.set_channel(dmx_chan+5, strobe_value) # strobe
