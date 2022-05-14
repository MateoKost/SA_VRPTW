import benchmarkReader
import algorithmFlow
import time
from Preliminaries import *


if __name__ == '__main__':
    directory = 'benchmarks/'
    capacityPath = 'benchmarks/vehicle_capacities.csv'
    dirs = benchmarkReader.getDirNames('benchmarks/')
    vehicleCapacities = benchmarkReader.readBenchmark(capacityPath)
    results = []
    for singleDir in dirs:
        files = benchmarkReader.getFileNames(f'{directory}{singleDir}/')
        for f in files:
            print(f)
            startTime = time.time()
            fdata = benchmarkReader.readBenchmark(f'{directory}{singleDir}/{f}')
            seriesVehicleCapacity = vehicleCapacities.loc[singleDir].CAPACITY
            totalDistance, nVehicles = algorithmFlow.run(f, fdata, seriesVehicleCapacity)
            duration = time.time() - startTime
            results.append([f, duration, totalDistance, nVehicles])
            print(f'duration - {duration}')
            # break for only one test flow
            break
    benchmarkReader.writeBenchmarkResults(results)