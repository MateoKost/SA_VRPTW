import pandas as pd
from os import walk, makedirs
from datetime import datetime


def getFileNames(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f


def readBenchmark(name):
    print(f'B - {name}')
    df = pd.read_csv(name, sep=';', index_col=0)
    return df


def writeBenchmarkResults(results):
    resultDf = pd.DataFrame(columns=['benchmark', 'duration', 'totalDistance', 'nVehicles'], data=results)
    makedirs('results', exist_ok=True)
    filename = "results/{}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    resultDf.to_csv(filename)


def generateRunName(benchmark, tzero, capacity):
    return f'{benchmark.split(".")[0]}_{datetime.now().strftime("%d%m%Y%H%M%S")}_T{tzero}_VC{capacity}'


def formatEpochResult():
    print('formatEpochResult')


def appendEpochResult(runName, fileName, result, header):
    columns = ['benchmark', 'epoch', 'temperature', 'totalDistance', 'nVehicles']

    if len(result[0]) < len(columns):
        resultDf = pd.DataFrame(columns=columns)
    else:
        resultDf = pd.DataFrame(columns=columns, data=result)
    makedirs(f'results/{runName}', exist_ok=True)
    resultDf.to_csv(f'results/{runName}/{fileName}', mode='a', header=header)


def writeEpochResult(runName, epoch, temperature, routes, mode):
    results = []
    for ri in range(0, len(routes)):
        results.append([routes[ri].index.tolist()])

    resultDf = pd.DataFrame(columns=['customers'], data=results)

    dirPath = f'results/{runName}/{mode}'
    makedirs(dirPath, exist_ok=True)
    filename = f'{dirPath}/ep{epoch}_T{temperature}.csv'
    resultDf.to_csv(filename)
