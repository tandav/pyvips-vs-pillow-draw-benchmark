from benchmark import config
from benchmark import render

for sink_name in ('ffmpeg', 'devnull'):
    for fps in (30, 60):
        config.fps = fps
        for w, h in [
            (426, 240),  # 240p
            (640, 360),  # 360p
            (854, 480),  # 480p
            (1280, 720),  # 720p
            (1920, 1080),  # 1080p
        ]:
            config.frame_width = w
            config.frame_height = h

            for backend in (render.Pillow, render.Vips):
                with open('logs/benchmark.jsonl', 'a') as log: print(backend(sink_name).render(), file=log)
