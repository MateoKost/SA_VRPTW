import pandas as pd


def readBenchmark(name):
    print(f'B - {name}')
    df = pd.read_csv(name, sep=';')
    return df
    # print(df)
