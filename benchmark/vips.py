import json
import random
import string
import sys
import time

import pyvips

import benchmark.sink as _sink
from benchmark import config
from benchmark import util


def render(n_frames, sink_name):
    bg = pyvips.Image.black(config.frame_width, config.frame_height, bands=3)
    background_draw = pyvips.Image.black(config.frame_width, config.frame_height, bands=3)

    colors = [util.hex_to_rgb(config.scale_colors[scale]) for scale in config.diatonic]
    chunk_width = config.frame_width
    frame_dx = chunk_width // n_frames
    x = 0
    chord_length = config.frame_width / 4
    t0 = time.time()

    with getattr(_sink, sink_name)() as sink:

        for frame in range(n_frames):
            x += frame_dx
            chord_i = int(x / chord_length)
            chord_start_px = int(chord_i * chord_length)
            background_color = random.choice(colors)

            # self.background_draw.rectangle((chord_start_px, 0, x + frame_dx, config.frame_height), fill=background_color)
            # self.background_draw = self.background_draw.draw_rect(background_color, chord_start_px, 0, x + frame_dx - chord_start_px, config.frame_height, fill=True)
            background_draw = background_draw.draw_rect(background_color, chord_start_px, 0, x - chord_start_px, config.frame_height, fill=True)

            # out = Image.alpha_composite(layer, self.background)
            out = (
                bg
                .composite2(background_draw, pyvips.enums.BlendMode.OVER, x=0, y=0)
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
                .insert(pyvips.Image.text(util.random_text()), *util.random_xy())
            )

            # q = ImageDraw.Draw(out)

            # q.text(util.rel_to_abs(0.28, 0), self.track.meta['bassline'], font=font, fill=text_color)
            # q.text(util.rel_to_abs(0, 0), f"score{self.track.meta['rhythm_score']}", font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0, 0.25), self.track.meta['chords'], font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0.58, 0.25), f"dist{self.track.meta['dist']}", font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0, 0.66), f"root scale: {self.track.meta['scale'].root.name} {self.track.meta['scale'].name}", font=font2, fill=text_color)
            # q.text((chord_start_px, util.rel_to_abs_h(0.75)), scale, font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0, 0.125), f"bass_decay{self.track.meta['bass_decay']}", font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0.47, 0.125), f'tuning{config.tuning}Hz', font=font2, fill=text_color)
            # q.text(util.rel_to_abs(0, 0.83), 'tandav.me', font=font, fill=text_color)
            # q.text(util.rel_to_abs(0.47, 0.85), sys.platform, font=font2, fill=text_color)

            # q.text((random.randrange(config.frame_width), random.randrange(config.frame_height)), random.choice(string.ascii_letters), font=font, fill=text_color)

            # q_video.put(random.choice(self.images), block=True)
            # self.q_video.put(out.tobytes(), block=True)
            # out.write_to_memory()
            sink.write(out.write_to_memory())

    dt = time.time() - t0
    fps = n_frames / dt
    speed = fps / config.fps
    return json.dumps({'backend': __name__.split('.')[1], 'sink': sink_name, 'dt': dt, 'fps': config.fps, 'actual_fps': fps, 'speed': speed, 'n_frames': n_frames, 'resolution': f'{config.frame_width}x{config.frame_height}', })

    # self.q_video.put(out.write_to_memory(), block=True)
    # self.q_video.append(out.write_to_memory())

# q_video.put(b''.join(random.choices(self.images, k=n_frames)), block=True)
# q_video.put(self.vbuff.getvalue(), block=True)
# self.frames_written += n_frames
# self.video_seconds_written += n_frames / config.fps
