import pandas as pd


def readBenchmark(name):
    print(f'B - {name}')
    df = pd.read_csv(name, sep=';', index_col=0)
    return df
    # print(df)
