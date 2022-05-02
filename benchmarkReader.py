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
