def lerp(a, b, dt, h):
    # smooth a to b
    return b + (a - b) * 2 ** (-dt / h)