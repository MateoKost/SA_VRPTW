import pandas as pd
from os import walk, makedirs
from datetime import datetime


def getFileNames(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f


def getDirNames(path):
    dirs = []
    for (dirpath, dirnames, filenames) in walk(path):
        dirs.extend(dirnames)
        break
    return dirs


def readBenchmark(name):
    print(f'B - {name}')
    df = pd.read_csv(name, sep=';', index_col=0)
    return df


def appendBenchmarkResults(results, destination, header):

    columns = ['benchmark', 'duration', 'totalDistance', 'nVehicles']

    if len(results[0]) < len(columns):
        resultDf = pd.DataFrame(columns=columns)
    else:
        resultDf = pd.DataFrame(columns=columns, data=results)

    makedirs(destination, exist_ok=True)
    filename = "{}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    filename = f'{destination}{filename}'
    resultDf.to_csv(filename, mode='a', header=header)


def generateStartName(tzero):
    return f'test_{datetime.now().strftime("%d%m%Y%H%M%S")}_T{tzero}'


def generateBenchmarkRunName(benchmark, tzero, capacity):
    return f'{benchmark.split(".")[0]}_{datetime.now().strftime("%d%m%Y%H%M%S")}_T{tzero}_VC{capacity}'


def appendEpochResult(exportDirectory, runName, fileName, result, header):
    columns = ['benchmark', 'epoch', 'temperature', 'totalDistance', 'nVehicles']

    if len(result[0]) < len(columns):
        resultDf = pd.DataFrame(columns=columns)
    else:
        resultDf = pd.DataFrame(columns=columns, data=result)
    makedirs(f'{exportDirectory}{runName}', exist_ok=True)
    resultDf.to_csv(f'{exportDirectory}{runName}/{fileName}', mode='a', header=header)


def writeEpochResult(exportDirectory, runName, epoch, temperature, routes, mode):
    results = []
    for ri in range(0, len(routes)):
        results.append([routes[ri].index.tolist()])

    resultDf = pd.DataFrame(columns=['customers'], data=results)

    dirPath = f'{exportDirectory}{runName}/{mode}'
    makedirs(dirPath, exist_ok=True)
    filename = f'{dirPath}/ep{epoch}_T{temperature}.csv'
    resultDf.to_csv(filename)
