# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import benchmarkReader
import readFiles
import algorithmFlow
import utils
import numpy as np
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    directory = 'benchmarks/';
    # files, duration = utils.measureTime(readFiles.getFileNames(directory))
    files = readFiles.getFileNames(directory)
    for f in files:
        print(f)
        startTime = time.time()
        fdata = benchmarkReader.readBenchmark(directory + f)
        # result, duration = utils.measureTime(algorithmFlow.run(fdata))
        result = algorithmFlow.run(fdata)
        # print(f'duration - {duration}')
        duration = time.time() - startTime
        print(f'duration - {duration}')
        break
        # break for only one test



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
