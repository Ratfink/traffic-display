import array
import gc

import ustruct
import machine

import png


class ImageError(Exception):
    pass

class TrafficDisplay:

    def __init__(self, speed=1, baudrate=80000000, le=None, oe=None, sck=None,
                 mosi=None, miso=None):
        self.oe = oe if oe is not None else machine.Pin(5, machine.Pin.OUT)
        self.le = le if le is not None else machine.Pin(4, machine.Pin.OUT)

        if sck is None and mosi is None and miso is None:
            self.spi = machine.SPI(0, baudrate=baudrate, polarity=0, phase=0)
        else:
            sck = sck if sck is not None else machine.Pin(14)
            mosi = mosi if mosi is not None else machine.Pin(13)
            miso = miso if miso is not None else machine.Pin(12)
            self.spi = machine.SPI(-1, baudrate=baudrate, polarity=0, phase=0,
                                   miso=miso, mosi=mosi, sck=sck)

        self.oev = self.oe.value
        self.lev = self.le.value

        self.oev(1)
        self.lev(0)

        self._linebufs = [
            bytearray((0xF1, 0xF0, 0xF0)),
            bytearray((0xF0, 0xF1, 0xF0)),
            bytearray((0xF0, 0xF0, 0xF1)),
            bytearray((0xF2, 0xF0, 0xF0)),
            bytearray((0xF0, 0xF2, 0xF0)),
            bytearray((0xF0, 0xF0, 0xF2)),
            bytearray((0xF4, 0xF0, 0xF0)),
            bytearray((0xF0, 0xF4, 0xF0)),
            bytearray((0xF0, 0xF0, 0xF4)),
            bytearray((0xF8, 0xF0, 0xF0)),
            bytearray((0xF0, 0xF8, 0xF0)),
            bytearray((0xF0, 0xF0, 0xF8))
        ]
        self._index = 0

        self.timer = machine.Timer(-1)
        self._timer_init_args = {'mode':machine.Timer.PERIODIC,
                                 'callback':self._refresh}

        self._speed = 0
        self.start(speed)

    def load_pbm(self, filename):
        state = self.stop()

        with open(filename, 'rb') as f:
            data = f.read()
        spd = data[:-24].split()
        if spd[0] != b'P4' or spd[-2] != b'12' or spd[-1] != b'12':
            raise ImageError()
        img = list(ustruct.unpack('>12H', data[-24:]))
        for i in range(len(img)):
            img[i] = img[i] >> 4
        self.update(img)

        del data, spd, img
        gc.collect()
        self.start(state)

    def load_png(self, filename):
        state = self.stop()

        reader = png.Reader(filename=filename)
        img = reader.read()
        if (img[0] != 12 or img[1] != 12 or not img[3]['greyscale'] or
                img[3]['alpha']):
            raise ImageError()
        shift = img[3]['bitdepth'] - 1
        tdimg = array.array('H')
        for row in img[2]:
            rowint = 0
            for i, pixel in enumerate(row):
                rowint |= (pixel >> shift) << 11 - i
            tdimg.append(rowint)
        self.update(tdimg)

        del reader, img, shift, tdimg
        gc.collect()
        self.start(state)

    def update(self, img):
        state = machine.disable_irq()
        for i, row in enumerate(img):
            for j in range(12):
                if (row >> j) & 1:
                    self._linebufs[i][2 - j%3] |= 0x10 << j//3
                else:
                    self._linebufs[i][2 - j%3] &= ~(0x10 << j//3)
        machine.enable_irq(state)

    def stop(self):
        if self._speed:
            self.timer.deinit()
            self.oev(1)
            self.lev(0)
            speed = self._speed
            self._speed = 0
            return speed
        return 0

    def start(self, state):
        if state:
            self.timer.init(period=state, **self._timer_init_args)
            self._speed = state
            self.oev(0)

    def _refresh(self, tim):
        self._index %= 12
        self.spi.write(self._linebufs[self._index])
        self.oev(1)
        self.lev(1)
        self.lev(0)
        self.oev(0)
        self._index += 1
