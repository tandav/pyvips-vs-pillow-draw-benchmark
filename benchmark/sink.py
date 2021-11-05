import contextlib
import subprocess
import random

from benchmark import config


@contextlib.contextmanager
def ffmpeg(fname):
    cmd = (
        'ffmpeg',
        # '-re',
        '-y',

        '-s', f'{config.frame_width}x{config.frame_height}',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgba',
        '-r', str(config.fps),  # input framrate
        '-i', '-',  # tell ffmpeg to expect video from the pipe

        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',

        '-vsync', 'cfr',
        '-b:v', '3m',
        '-deinterlace',
        '-r', str(config.fps),  # output framerate
        '-f', 'flv',
        '-flvflags', 'no_duration_filesize',
        f'/tmp/{fname}.flv',
    )

    _ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    yield _ffmpeg.stdin
    _ffmpeg.communicate()
    _ffmpeg.wait()


@contextlib.contextmanager
def devnull(fname):
    f = open('/dev/null', 'wb')
    yield f
    f.close()
