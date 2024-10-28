from lib_psg import load_yaml, load_config, load_fixtures, check_dmx_consistency
from physical_light import PhysicalLight
from group_of_lights import GroupOfLights
from dmxlib import Dmx, FakeDmx
import time, random, sys, os, threading
from infinite_timer import InfiniteTimer
import globalz
import mido


conf = 'Conf/config.yaml' if len(sys.argv) == 1 else sys.argv[1]

config = load_config(conf)
ui = load_yaml('Conf/ui.yaml')
fixtures = load_fixtures(config)

check_dmx_consistency(config, fixtures)

try:
    dmx = Dmx(os.environ['SERIAL_PORT']) # note device serial in the connect string //usbserial-A50285BI
except:
    dmx = FakeDmx(34,1)

globalz.window = {}

physical_lights_and_groups = {
    l['name']: PhysicalLight(l['name'], l['channel'], fixtures[l['name']], dmx) for l in config['lights']
}
for ui_item in config['layout']['components']:
    if 'group' in ui_item:
        name = ui_item['group']
        physical_lights_and_groups[name] = GroupOfLights(name, ui_item['components'], physical_lights_and_groups)
# print(physical_lights_and_groups)


auto_mode_t0 = None

def auto_mode_tick(threshold, fade_time):
    global auto_mode_t0, physical_lights_and_groups
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

def global_tick():
    global auto_mode, physical_lights_and_groups
    if auto_mode:
        auto_mode_tick(3, 5)
    for l in physical_lights_and_groups.values():
        # print('.', end='', flush=True)
        l.tick()


timer_thread = InfiniteTimer(0.050, global_tick)
timer_thread.start()

auto_mode = True
auto_mode_t0 = time.time()
for l in physical_lights_and_groups.values():
    l.set_dimmer(255)

with mido.open_input('nanoKONTROL2 SLIDER/KNOB') as port:
    is_running = True
    while is_running:
        print('running')
        for msg in port.iter_pending():
            print(msg, type(msg))
            print(msg.control)
            print(msg.value)
            if msg.control == 42 and msg.value == 127:
                is_running = False

        time.sleep(1)

timer_thread.cancel()
dmx.blackout()
dmx.stop()
