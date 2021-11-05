from benchmark import config


def hex_to_rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgba_to_rgb(rgb_background, rgba_color):
    '''https://stackoverflow.com/a/21576659/4204843'''

    alpha = rgba_color[3]

    return (
        int((1 - alpha) * rgb_background[0] + alpha * rgba_color[0]),
        int((1 - alpha) * rgb_background[1] + alpha * rgba_color[1]),
        int((1 - alpha) * rgb_background[2] + alpha * rgba_color[2]),
    )


def minmax_scaler(value, oldmin, oldmax, newmin=0.0, newmax=1.0):
    '''
    >>> minmax_scaler(50, 0, 100, 0.0, 1.0)
    0.5
    '''
    return (value - oldmin) * (newmax - newmin) / (oldmax - oldmin) + newmin


def rel_to_abs_w(value): return int(minmax_scaler(value, 0, 1, 0, config.frame_width))
def rel_to_abs_h(value): return int(minmax_scaler(value, 0, 1, 0, config.frame_height))


def rel_to_abs(x, y):
    """xy: coordinates in fractions of screen"""
    return rel_to_abs_w(x), rel_to_abs_h(y)
