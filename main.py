import benchmarkReader
import algorithmFlow
import time
from Preliminaries import *


if __name__ == '__main__':
    directory = 'benchmarks/C1/';
    files = benchmarkReader.getFileNames(directory)
    results = []
    for f in files:
        print(f)
        startTime = time.time()
        fdata = benchmarkReader.readBenchmark(directory + f)
        totalDistance, nVehicles = algorithmFlow.run(f, fdata, VEHICLE_CAPACITY_C1)
        duration = time.time() - startTime
        results.append([f, duration, totalDistance, nVehicles])
        print(f'duration - {duration}')
        # break for only one test flow
        break
    benchmarkReader.writeBenchmarkResults(results)