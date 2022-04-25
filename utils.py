# import timeit
import time


def measureTime(f):
    startTime = time.time()
    result = f
    duration = time.time() - startTime
    duration *= 1000.0
    # print('function took {:f} ms'.format(duration))
    return result, duration


    # result = timeit.timeit(lambda: f, number=1)
    # print('%s function took %0.2f ms'.format(f.__name__, result * 1000.0))

