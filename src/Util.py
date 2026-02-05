import numpy as np


def lerp(a, b, dt, h):
    # smooth a to b
    return b + (a - b) * 2 ** (-dt / h)

def approach(val, target, max_move):
    val = np.asarray(val)
    return np.where(
        val > target,
        np.maximum(val - max_move, target),
        np.minimum(val + max_move, target)
    )