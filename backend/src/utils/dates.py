import time


def timestamp_ms() -> int:
    return int(time.time() * 1000)
