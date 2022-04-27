# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Preliminaries
import benchmarkReader
import readFiles
import algorithmFlow
import utils
import numpy as np
import time
from Preliminaries import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    directory = 'benchmarks/C1/';
    # files, duration = utils.measureTime(readFiles.getFileNames(directory))
    files = readFiles.getFileNames(directory)
    for f in files:
        print(f)
        startTime = time.time()
        fdata = benchmarkReader.readBenchmark(directory + f)
        # result, duration = utils.measureTime(algorithmFlow.run(fdata))
        result = algorithmFlow.run(fdata, VEHICLE_CAPACITY_C1)
        # print(f'duration - {duration}')
        duration = time.time() - startTime
        print(f'duration - {duration}')
        break
        # break for only one test flow



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
