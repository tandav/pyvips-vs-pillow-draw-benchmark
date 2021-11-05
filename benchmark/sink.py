import contextlib
import subprocess

from benchmark import config


@contextlib.contextmanager
def ffmpeg():
    cmd = ('ffmpeg',
           '-re',
           '-y',

           '-s', f'{config.frame_width}x{config.frame_height}',  # size of image string
           '-f', 'rawvideo',
           '-pix_fmt', 'rgba',  # format
           '-r', str(config.fps),  # input framrate. This parameter is important to stream w/o memory overflow
           # '-vsync', 'cfr', # kinda optional but you can turn it on
           # '-f', 'image2pipe',
           # '-i', 'pipe:', '-', # tell ffmpeg to expect raw video from the pipe
           # '-i', '-',  # tell ffmpeg to expect raw video from the pipe
           # '-thread_queue_size', thread_queue_size,
           # '-blocksize', '2048',
           '-i', '-',  # tell ffmpeg to expect raw video from the pipe

           # '-c:a', 'libvorbis',
           # '-ac', '1',  # number of audio channels (mono1/stereo=2)
           # '-c:v', 'h264_videotoolbox',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           # '-tune', 'animation',

           # ultrafast or zerolatency kinda makes audio and video out of sync when save to file (but stream to yt is kinda OK)
           # '-preset', 'ultrafast',
           # '-tune', 'zerolatency',

           # '-g', '150',  #  GOP: group of pictures
           # '-g', str(keyframe_seconds * config.fps),  # GOP: group of pictures
           # '-g', str(config.fps // 2),  # GOP: group of pictures
           '-x264opts', 'no-scenecut',
           # '-x264-params', f'keyint={keyframe_seconds * config.fps}:scenecut=0',
           '-vsync', 'cfr',
           # '-async', '1',
           # '-tag:v', 'hvc1', '-profile:v', 'main10',
           # '-b:v', '16M',
           # '-b:a', "300k",
           # '-b:a', '128k',
           # '-b:v', '64k',
           '-b:v', config.video_bitrate,
           # '-b:v', '12m',
           '-deinterlace',
           # '-r', str(config.fps),

           '-r', str(config.fps),  # output framerate
           # '-maxrate', '1000k',
           # '-map', '0:a',
           # '-map', '1:v',

           # '-b', '400k', '-minrate', '400k', '-maxrate', '400k', '-bufsize', '1835k',
           # '-b', '400k', '-minrate', '400k', '-maxrate', '400k', '-bufsize', '300m',

           # '-blocksize', '2048',
           # '-flush_packets', '1',
           '-f', 'flv',
           '-flvflags', 'no_duration_filesize',
           '/tmp/output.flv',
           )

    _ffmpeg = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    yield _ffmpeg.stdin
    _ffmpeg.communicate()
    _ffmpeg.wait()


@contextlib.contextmanager
def devnull():
    f = open('/dev/null', 'wb')
    yield f
    f.close()