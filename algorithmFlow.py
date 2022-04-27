from Preliminaries import *
import utils
import math
import pandas as pd


def run(fdata, vehicle_capacity):
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
    EE_CUSTOMERS = EE_CUSTOMERS.sort_values(by=['WINDOW_LENGTH'], ascending=True)

    # mt/lt customers
    MT_CUSTOMERS = EE_CUSTOMERS.head(MT_CLIENT_C1)
    LT_CUSTOMERS = EE_CUSTOMERS.tail(LT_CLIENT_C1)

    # retieve Everyone Else
    EE_CUSTOMERS.drop(MT_CUSTOMERS.index, axis=0, inplace=True)
    EE_CUSTOMERS.drop(LT_CUSTOMERS.index, axis=0, inplace=True)

    print(MT_CUSTOMERS)
    # print(LT_CUSTOMERS)
    # print(EE_CUSTOMERS)

    # specify new vehicle route
    route = pd.DataFrame(columns=depot.columns, index=depot.index)
    route = route.dropna()

    # first route
    RW = 0
    TT = 0
    VC = 0

    for i in range(0, len(MT_CUSTOMERS)):
        c = MT_CUSTOMERS.iloc[[i]]
        next_VC = VC + c['DEMAND'].values[0]
        if next_VC > vehicle_capacity:
            continue
        VC = next_VC
        route = pd.concat([route, c], ignore_index=False, axis=0)


    print(route)

    # for row in MT_CUSTOMERS.itertuples():
        # print(row)
        # total.append(row.src_bytes + row.dst_bytes)


    # for index, c in MT_CUSTOMERS.iterrows():
    #     next_VC = VC + c['DEMAND']
    #     if next_VC > vehicle_capacity:
    #         continue
    #     VC = next_VC
        # route.concat(c)
        # route = pd.concat([route, c], ignore_index=True, axis=1)
        # route.append(c, ignore_index=False)
        # route[0,index] = c


        # print(MT_CUSTOMERS.iloc(1,))

        # route.iloc[index] = c
        # print(VC)

        # RT = c['READY TIME']
        # TT = TT if TT <= RT else RT
        # TT += c['SERVICE TIME']

    # print(route)

    # print(fdata)

    # tour = fdata["CUST NO."].values
    # print(tour)
    # distance = totaldistancetour(fdata, tour)
    # print(f'distance - {distance}')

    # min distance
    #


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
