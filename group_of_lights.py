import globalz

class GroupOfLights:
    def __init__(self, name: str, components: list, physical_lights: list):
        self.name = name
        print(components)
        self.components = [ physical_lights[c] for c in components ]

    def __repr__(self):
        return f'{self.name}: {self.components}\n'

    def set_next_color(self, color_code: str, fade_time: float):
        for c in self.components:
            c.set_next_color(color_code, fade_time)

    def set_dimmer(self, dimmer: int):
        for c in self.components:
            c.set_dimmer(dimmer)
            # globalz.window[f'DIMMER_{c.name}'].update(value=dimmer)

    def set_strobe(self, strobe: int):
        for c in self.components:
            c.set_strobe(strobe)
            # globalz.window[f'STROBE_{c.name}'].update(value=strobe)


    def tick(self):
        pass