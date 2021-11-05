import json
import random
import time

from PIL import Image
from PIL import ImageDraw

import benchmark.sink as _sink
from benchmark import config
from benchmark import util


def render(n_frames, sink_name):
    layer = Image.new('RGBA', (config.frame_width, config.frame_height), (255, 255, 255, 0))
    text_color = (0, 0, 0)

    background = Image.new('RGBA', layer.size, (200, 200, 200))
    background_draw = ImageDraw.Draw(background)


    # colors = [util.hex_to_rgb(config.scale_colors[scale]) for scale in config.diatonic]
    chunk_width = config.frame_width
    frame_dx = chunk_width // n_frames
    x = 0
    chord_length = config.frame_width / 4
    t0 = time.time()
    fname = f'{__name__.split(".")[1]}-{config.frame_width}x{config.frame_height}-{config.fps}fps-{random.randint(10000, 99999)}'
    with getattr(_sink, sink_name)(fname) as sink:
        for frame in range(n_frames):
            x += frame_dx
            chord_i = int(x / chord_length)
            chord_start_px = int(chord_i * chord_length)
            # background_color = random.choice(colors)
            background_color = (random.randrange(255), random.randrange(255), random.randrange(255))
            # background_draw.rectangle((chord_start_px, 0, x + frame_dx, config.frame_height), fill=background_color)

            for _ in range(8):
                x0 = random.randrange(config.frame_width)
                y0 = random.randrange(config.frame_height)
                x1 = random.randrange(config.frame_width)
                y1 = random.randrange(config.frame_height)
                background_draw.rectangle((x0, y0, x1, y1), fill=background_color)


            out = Image.alpha_composite(layer, background)
            q = ImageDraw.Draw(out)

            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            q.text(util.random_xy(), util.random_text(), fill=text_color)
            sink.write(out.tobytes())

    dt = time.time() - t0
    fps = n_frames / dt
    speed = fps / config.fps
    return json.dumps({'backend': __name__.split('.')[1], 'sink': sink_name, 'dt': dt, 'fps': config.fps, 'actual_fps': fps, 'speed': speed, 'n_frames': n_frames, 'resolution': f'{config.frame_width}x{config.frame_height}', })
