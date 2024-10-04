
from PyQt6 import QtWidgets, QtCore, QtGui

class Konsol(QtWidgets.QMainWindow):
    def __init__(self, config, fixtures, ui, app: QtWidgets.QApplication):
        self.config = config
        self.fixtures = fixtures
        self.ui = ui
        self.app = app

        QtWidgets.QMainWindow.__init__(self, None)
        self.setWindowTitle("Konsol")
        self.init_create_ui()

    def init_create_ui(self):
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.hboxes = []
        self.vbox = QtWidgets.QVBoxLayout()
        for ui_item in self.config['layout']['components']:
            self.build_controls(ui_item)

        self.widget.setLayout(self.vbox)

    
    def build_controls(self, ui_item):
        if 'light' in ui_item:
            item_name = ui_item['light']
            light = self.fixtures[item_name]
            self.build_light_controls(item_name, light)
        elif 'group' in ui_item:
            self.build_group_controls(ui_item)
        else:
            raise ValueError('conf error')

    def build_light_controls(self, item_name, light):
        hbox = QtWidgets.QHBoxLayout()

        hbox.addWidget(QtWidgets.QLabel(item_name))

        self.vbox.addLayout(hbox)

    def build_group_controls(self, ui_item):
        controls = []
        # controls.append(sg.Text(group['group'], justification='right', size=ui_sizes['text']))

        # can_rgb = all([fixtures[c]['can_rgb'] for c in group['components']])
        # can_white = all([fixtures[c]['can_white'] for c in group['components']])
        # can_amber = all([fixtures[c]['can_amber'] for c in group['components']])
        # controls.extend(build_color_buttons(group["group"], colors, can_rgb, can_white, can_amber, ui_sizes))

    def build_color_buttons(name: str, colors: list, can_rgb: bool, can_white: bool, can_amber: bool, ui_sizes: dict) -> list:
        buttons = []
        # buttons.append(sg.Slider(orientation='h', key=f'DIMMER_{name}', enable_events=True, range=(0,255), resolution=1, default_value=255, size=(ui_sizes['dimmer_w'],ui_sizes['dimmer_h'])))
        # for color in colors:
        #     c = color['display']
        #     if (color['rgb'] and can_rgb) or (color['white'] and can_white) or (color['amber'] and can_amber):
        #         tooltip = color['label'] if 'label' in color else ''
        #         b = sg.Button(button_color=('black', c), mouseover_colors=c, tooltip=tooltip,
        #             key=f'COLOR_{name}_{color["code"]}', size=(ui_sizes['button_w'], ui_sizes['button_h']), pad=((0,0),(0,1)), border_width=0)
        #     else:
        #         b = sg.B(size=(ui_sizes['button_w'], ui_sizes['button_h']), pad=((0,0),(0,1)), border_width=0, disabled=True)
        #     buttons.append(b)
        # buttons.append(sg.Slider(orientation='h', key=f'STROBE_{name}', enable_events=True, range=(0,255), resolution=1, default_value=0, size=(ui_sizes['dimmer_w'],ui_sizes['dimmer_h'])))

        # self.timer = QtCore.QTimer(self)
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.dmx_timer)
        # self.timer.stop()
