from benchmark import config
from benchmark import render

for sink_name in ('ffmpeg', 'devnull'):
    for fps in (30, 60):
        config.fps = fps
        for w, h in [
            (426, 240),
            (640, 360),
            (854, 480),
            (1280, 720),
            (1920, 1080),
        ]:
            config.frame_width = w
            config.frame_height = h

            for backend in (render.Vips, render.Pillow):
                with open('logs/benchmark.jsonl', 'a') as log: print(backend(sink_name).render(), file=log)
