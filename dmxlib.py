import sys, time, threading
import pyftdi.serialext


class Dmx:
    def __init__(self, serial_port):
        print('INITIALIZE Dmx object')
        try:
            self.serial = pyftdi.serialext.serial_for_url(serial_port, baudrate=250000, stopbits=2)
        except:
            print("Error: could not open Serial Port")
            sys.exit(0)
        self.dmx_data = [bytes([0])] * 513
        self.dmx_data[0] = bytes([0])
        self.run = True
        self.dmx_thread = threading.Thread(target=self.display_universe)
        self.dmx_thread.start()

    def stop(self):
        self.run = False

    def set_channel(self, chan, intensity):
        if chan > 512: chan = 512
        if chan < 0: chan = 0
        if intensity > 255: intensity = 255
        if intensity < 0: intensity = 0
        self.dmx_data[chan] = bytes([intensity])
        
    def blackout(self):
        for i in range(1, 512, 1):
            self.dmx_data[i] = bytes([0])
        
    def render(self):
        sdata = b''.join(self.dmx_data)
        self.serial.send_break(duration=0.001)
        self.serial.write(sdata)

    def display_universe(self):
        while self.run:
            self.render()
            time.sleep(0.005)

class FakeDmx:
    def __init__(self,chan_max, timer=1.0):
        self.dmx_data = [bytes([0])] * 513
        self.dmx_data[0] = bytes([0])
        self.timer = timer
        self.run = True
        self.chan_max = chan_max
        self.dmx_thread = threading.Thread(target=self.display_universe)
        self.dmx_thread.start()

    def stop(self):
        self.run = False

    def set_channel(self, chan, intensity):
        if chan > 512: chan = 512
        if chan < 0: chan = 0
        if intensity > 255: intensity = 255
        if intensity < 0: intensity = 0
        self.dmx_data[chan] = bytes([intensity])
        
    def blackout(self):
        for i in range(1, 512, 1):
            self.dmx_data[i] = bytes([0])
        
    def render(self):
        print(' '.join(x.hex() for x in self.dmx_data[:self.chan_max]))

    def display_universe(self):
        while self.run:
            self.render()
            time.sleep(self.timer)


