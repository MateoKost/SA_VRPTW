from Preliminaries import *
import utils
import math
import pandas as pd
import initialSolution


def run(fdata, VEHICLE_CAPACITY):
    # decrease indexes () by 1
    fdata.index -= 1

    # specify and remove depot
    depot = fdata.head(1)
    fdata.drop(depot.index, axis=0, inplace=True)
    print(f'depot - {depot}')

    # calculate time windows
    fdata['WINDOW_LENGTH'] = fdata.apply(lambda row: row['DUE DATE'] - row['READY TIME'], axis=1)

    # operate on fdata (raw data) copy
    EE_CUSTOMERS = fdata.copy()

    # sort customers by windows
    EE_CUSTOMERS = EE_CUSTOMERS.sort_values(by=['WINDOW_LENGTH', 'READY TIME', 'DUE DATE'], ascending=[True, True, True])

    # mt/lt customers
    MT_CUSTOMERS = EE_CUSTOMERS.head(MT_CLIENT_C1)
    LT_CUSTOMERS = EE_CUSTOMERS.tail(LT_CLIENT_C1)

    # retrieve Everyone Else
    EE_CUSTOMERS.drop(MT_CUSTOMERS.index, axis=0, inplace=True)
    EE_CUSTOMERS.drop(LT_CUSTOMERS.index, axis=0, inplace=True)

    # get initial solution
    initialSolution.flow(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, VEHICLE_CAPACITY)

    # tour = fdata["CUST NO."].values
    # print(tour)
    # distance = totaldistancetour(fdata, tour)
    # print(f'distance - {distance}')



def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def totaldistancetour(customers, tour):
    d = 0
    for i in range(1, len(tour)):
        customerPrevious = customers[customers['CUST NO.'] == tour[i - 1]]
        x1 = customerPrevious['XCOORD.'].values[0]
        y1 = customerPrevious['YCOORD.'].values[0]

        customerAtTourMoment = customers[customers['CUST NO.'] == tour[i]]
        x2 = customerAtTourMoment['XCOORD.'].values[0]
        y2 = customerAtTourMoment['YCOORD.'].values[0]

        d = d + distance(x1, y1, x2, y2)
    return d
