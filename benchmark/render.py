import abc
import json
import random
import time

import pyvips
from PIL import Image
from PIL import ImageDraw

import benchmark.sink as _sink
from benchmark import config
from benchmark import util


class Render(abc.ABC):
    def __init__(self, sink_name):
        self.sink_name = sink_name
        self.backend = None

    def render(self):
        t0 = time.time()

        fname = f'{self.backend}-{config.frame_width}x{config.frame_height}-{config.fps}fps'
        with getattr(_sink, self.sink_name)(fname) as sink:
            for frame in range(config.n_frames):
                self.write_frame(sink)
        dt = time.time() - t0
        fps = config.n_frames / dt
        speed = fps / config.fps
        return json.dumps({
            'backend': self.backend, 'sink': self.sink_name, 'dt': dt, 'fps': config.fps, 'actual_fps': fps,
            'speed': speed, 'n_frames': config.n_frames, 'resolution': f'{config.frame_width}x{config.frame_height}', })

    @abc.abstractmethod
    def write_frame(self, sink): ...


class Vips(Render):
    def __init__(self, sink_name):
        super().__init__(sink_name)
        self.backend = 'vips'
        self.bg = pyvips.Image.black(config.frame_width, config.frame_height, bands=3)
        self.background_draw = pyvips.Image.black(config.frame_width, config.frame_height, bands=3)

    def write_frame(self, sink):
        background_color = util.random_color()
        for _ in range(8):
            x, y = util.random_xy()
            w = random.randrange(config.frame_width - x)
            h = random.randrange(config.frame_height - y)
            self.background_draw = self.background_draw.draw_rect(background_color, x, y, w, h, fill=True)
        out = self.bg.composite2(self.background_draw, pyvips.enums.BlendMode.OVER, x=0, y=0)
        for _ in range(8):
            out = out.insert(pyvips.Image.text(util.random_text()), *util.random_xy())
        sink.write(out.write_to_memory())


class Pillow(Render):
    def __init__(self, sink_name):
        super().__init__(sink_name)
        self.backend = 'pillow'
        self.layer = Image.new('RGBA', (config.frame_width, config.frame_height), (255, 255, 255, 0))
        self.background = Image.new('RGBA', self.layer.size, (200, 200, 200))
        self.background_draw = ImageDraw.Draw(self.background)

    def write_frame(self, sink):
        background_color = util.random_color()
        for _ in range(8):
            self.background_draw.rectangle((util.random_xy(), util.random_xy()), fill=background_color)
        out = Image.alpha_composite(self.layer, self.background)
        q = ImageDraw.Draw(out)
        for _ in range(8):
            q.text(util.random_xy(), util.random_text())
        sink.write(out.tobytes())
