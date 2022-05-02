import time


def measureTime(f):
    startTime = time.time()
    result = f
    duration = time.time() - startTime
    duration *= 1000.0
    return result, duration

