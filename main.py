import benchmarkReader
import algorithmFlow
import time
from Preliminaries import *


if __name__ == '__main__':
    benchmarkDirectoryPath = 'benchmarks/'
    capacityPath = 'benchmarks/vehicle_capacities.csv'
    dirs = benchmarkReader.getDirNames('benchmarks/')
    vehicleCapacities = benchmarkReader.readBenchmark(capacityPath)
    startName = benchmarkReader.generateStartName(TZERO)
    results = []
    exportDirectory = f'results/{startName}/'
    benchmarkReader.appendBenchmarkResults([[]], exportDirectory, True)
    for singleDir in dirs:
        files = benchmarkReader.getFileNames(f'{benchmarkDirectoryPath}{singleDir}/')
        for f in files:
            print(f)
            startTime = time.time()
            fdata = benchmarkReader.readBenchmark(f'{benchmarkDirectoryPath}{singleDir}/{f}')
            seriesVehicleCapacity = vehicleCapacities.loc[singleDir].CAPACITY
            totalDistance, nVehicles = algorithmFlow.run(f'{exportDirectory}{singleDir}/',
                                                         f, fdata, seriesVehicleCapacity)
            duration = time.time() - startTime
            results.append([f, duration, totalDistance, nVehicles])
            print(f'duration - {duration}')
            benchmarkReader.appendBenchmarkResults(results, exportDirectory, False)
