import PySimpleGUI as sg
from lib import load_yaml, load_config, load_fixtures, build_layout, check_dmx_consistency
from physical_light import PhysicalLight
from group_of_lights import GroupOfLights
from dmxlib import Dmx, FakeDmx
import time, random, sys

import globalz
conf = 'Conf/config.yaml' if len(sys.argv) == 1 else sys.argv[1]

config = load_config(conf)
ui = load_yaml('Conf/ui.yaml')
fixtures = load_fixtures(config)

check_dmx_consistency(config, fixtures)

try:
    dmx = Dmx('ftdi://ftdi:232:A50285BI/1') # note device serial in the connect string //usbserial-A50285BI
except:
    dmx = FakeDmx(34,1)


physical_lights_and_groups = {
    l['name']: PhysicalLight(l['name'], l['channel'], fixtures[l['name']], dmx) for l in config['lights']
}
for ui_item in config['layout']['components']:
    if 'group' in ui_item:
        name = ui_item['group']
        physical_lights_and_groups[name] = GroupOfLights(name, ui_item['components'], physical_lights_and_groups)
# print(physical_lights_and_groups)

layout = build_layout(config, fixtures, ui)

globalz.window = sg.Window('Konsol', layout, resizable=True, finalize=True)
timer_id = globalz.window.timer_start(1)

auto_mode_t0 = None

def auto_mode_tick(threshold, fade_time):
    global auto_mode_t0
    if auto_mode_t0:
        interval = time.time() - auto_mode_t0
        if interval >= threshold:
            auto_mode_t0 = time.time()
            for l in physical_lights_and_groups.values():
                if isinstance(l, PhysicalLight) and l.fixture['can_rgb']:
                    red=random.randint(0,255)
                    green=random.randint(0,255)
                    blue=random.randint(0,255)
                    color_code = f'{red:02x}{green:02x}{blue:02x}0000'
                    l.set_next_color(color_code, fade_time)



auto_mode = False
while True:
    event, values = globalz.window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    # print(event)
    if event.startswith('COLOR_'):
        _,name,color_code = event.split('_')
        physical_lights_and_groups[name].set_next_color(color_code, values['FADE_TIME'])
    elif event.startswith('DIMMER_'):
        _,name = event.split('_')
        physical_lights_and_groups[name].set_dimmer(int(values[event]))
    elif event.startswith('STROBE_'):
        _,name = event.split('_')
        physical_lights_and_groups[name].set_strobe(int(values[event]))
    elif event == '__TIMER EVENT__':
        if auto_mode:
            auto_mode_tick(values['AUTO_TIME'], values['AUTO_FADE_TIME'])
        for l in physical_lights_and_groups.values():
            l.tick()
    elif event == 'AUTO':
        auto_mode = not auto_mode
        globalz.window['AUTO'].update(text="AUTO ON" if auto_mode else "AUTO OFF")
        globalz.window['AUTO'].update(button_color='white on green' if auto_mode else 'white on red')
        if auto_mode:
            auto_mode_t0 = time.time()


dmx.blackout()
dmx.stop()
globalz.window.close()
