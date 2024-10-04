import yaml
import PySimpleGUI as sg

def load_yaml(yaml_file: str) -> dict:
    with open(yaml_file, 'r') as file:
        content = yaml.safe_load(file)
        return content


def load_config(yaml_file: str) -> dict:
    return load_yaml(yaml_file)


def load_fixtures(config: dict) -> dict:
    return {
        light['name']: load_yaml(light['fixture']) for light in config['lights']
    }

def build_color_buttons(name: str, colors: list, can_rgb: bool, can_white: bool, can_amber: bool, ui_sizes: dict) -> list:
    buttons = []
    buttons.append(sg.Slider(orientation='h', key=f'DIMMER_{name}', enable_events=True, range=(0,255), resolution=1, default_value=255, size=(ui_sizes['dimmer_w'],ui_sizes['dimmer_h'])))
    for color in colors:
        c = color['display']
        if (color['rgb'] and can_rgb) or (color['white'] and can_white) or (color['amber'] and can_amber):
            tooltip = color['label'] if 'label' in color else ''
            b = sg.Button(button_color=('black', c), mouseover_colors=c, tooltip=tooltip,
                key=f'COLOR_{name}_{color["code"]}', size=(ui_sizes['button_w'], ui_sizes['button_h']), pad=((0,0),(0,1)), border_width=0)
        else:
            b = sg.B(size=(ui_sizes['button_w'], ui_sizes['button_h']), pad=((0,0),(0,1)), border_width=0, disabled=True)
        buttons.append(b)
    buttons.append(sg.Slider(orientation='h', key=f'STROBE_{name}', enable_events=True, range=(0,255), resolution=1, default_value=0, size=(ui_sizes['dimmer_w'],ui_sizes['dimmer_h'])))
    return buttons

def build_light_controls(item_name: str, light: dict, colors: list, ui_sizes: dict) -> list:
    controls = []
    controls.append(sg.Text(item_name, justification='right', size=ui_sizes['text']))
    controls.extend(build_color_buttons(item_name, colors, light['can_rgb'], light['can_white'], light['can_amber'], ui_sizes))
    return controls

def build_group_controls(group: dict, colors: list, fixtures: dict, ui_sizes: dict) -> list:
    controls = []
    controls.append(sg.Text(group['group'], justification='right', size=ui_sizes['text']))

    can_rgb = all([fixtures[c]['can_rgb'] for c in group['components']])
    can_white = all([fixtures[c]['can_white'] for c in group['components']])
    can_amber = all([fixtures[c]['can_amber'] for c in group['components']])
    controls.extend(build_color_buttons(group["group"], colors, can_rgb, can_white, can_amber, ui_sizes))
    return controls

def build_controls(ui_item, colors: list, fixtures: list, ui_sizes: dict) -> list:
    if 'light' in ui_item:
        item_name = ui_item['light']
        light = fixtures[item_name]
        controls = build_light_controls(item_name, light, colors, ui_sizes)
    elif 'group' in ui_item:
        controls = build_group_controls(ui_item, colors, fixtures, ui_sizes)
    else:
        raise ValueError('conf error')

    return controls

def build_layout(config: dict, fixtures: dict, ui: dict) -> list:
    layout = []
    for ui_item in config['layout']['components']:
        row = []
        controls = build_controls(ui_item, ui['colors'], fixtures, ui['sizes'])
        row.extend(controls)
        layout.append(row)
    layout.append([
        sg.Text('Fade time', justification='right', size=ui['sizes']['text']),
        sg.Slider(orientation='h', default_value=1.0, key='FADE_TIME', enable_events=True, range=(0,3.0), resolution=0.01, tick_interval=1.0, expand_x=True)
    ])
    layout.append([sg.HorizontalSeparator(color='#508080')])

    layout.append(
        [
            sg.Col(
                [
                    [
                        sg.Text('Auto time', justification='right', size=ui['sizes']['text']), sg.Slider(orientation='h', default_value=1.0, key='AUTO_TIME', enable_events=True, range=(0,3.0), resolution=0.01, tick_interval=1.0, expand_x=True)
                    ],
                    [
                        sg.Text('Auto fade time', justification='right', size=ui['sizes']['text']), sg.Slider(orientation='h', default_value=1.0, key='AUTO_FADE_TIME', enable_events=True, range=(0,3.0), resolution=0.01, tick_interval=1.0, expand_x=True)
                    ]
                ], expand_x=True
            ),
            sg.Col(
                [
                    [
                        sg.Button("AUTO OFF", button_color=('white on grey'),
                            key='AUTO', size=(ui['sizes']['big_button_w'],
                            ui['sizes']['big_button_h']), pad=0)

                    ]
                ]
            )
        ]
    )

    layout.append([sg.HorizontalSeparator(color='#508080')])
    layout.append([sg.Button('Quit')])
    return layout


def check_dmx_consistency(config: dict, fixtures: dict):
    channels = [0]*512
    for l in config['lights']:
        nb = fixtures[l['name']]['channels']['nb']
        for c in range(l['channel'], nb+1):
            if c < 0 or c > 512:
                raise IndexError(f'{l["name"]} has incorrect channel specification')
            channels[c-1] += 1
            if channels[c-1] > 1:
                raise ValueError(f'{l["name"]} conflicts with previous fixture')
