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
    EE_CUSTOMERS = EE_CUSTOMERS.sort_values(by=['WINDOW_LENGTH', 'READY TIME', 'DUE DATE'], ascending=[True, True, True])

    # mt/lt customers
    MT_CUSTOMERS = EE_CUSTOMERS.head(MT_CLIENT_C1)
    LT_CUSTOMERS = EE_CUSTOMERS.tail(LT_CLIENT_C1)

    # retrieve Everyone Else
    EE_CUSTOMERS.drop(MT_CUSTOMERS.index, axis=0, inplace=True)
    EE_CUSTOMERS.drop(LT_CUSTOMERS.index, axis=0, inplace=True)

    print(MT_CUSTOMERS)
    # print(LT_CUSTOMERS)
    # print(EE_CUSTOMERS)

    # specify new vehicle route
    route = pd.DataFrame(columns=depot.columns, index=depot.index)
    route = route.dropna()

    # first route

    # Total Time
    TT = 0
    # Vehicle Capacity
    VC = 0

    for MTi in range(0, len(MT_CUSTOMERS)):
        # get i-th customer
        c = MT_CUSTOMERS.iloc[[MTi]]
        next_VC = VC + c['DEMAND'].values[0]

        # customers param values
        RT = c['READY TIME'].values[0]
        DT = c['DUE DATE'].values[0]
        ST = c['SERVICE TIME'].values[0]

        # check if vehicle capacity with current customer demand is available or DUE DATE isn't reached
        # if not skip to next customer
        if next_VC > vehicle_capacity or TT > DT:
            continue

        # (optional) update total time by RT
        if TT <= RT:
            TT = RT

        # increment total time by customer service time
        TT += ST
        # increment vehicle capacity
        VC = next_VC

        # place customer at route
        route = pd.concat([route, c], ignore_index=False, axis=0)


    # remove aligned customers from MT_CUSTOMERS
    MT_CUSTOMERS.drop(route.index, axis=0, inplace=True)

    print(route)

    # check LT_CUSTOMERS

    # Total Time
    TT = 0
    # Vehicle Capacity
    VC = 0

    # for LTi in range(0, len(LT_CUSTOMERS)):
    #
    #     # get i-th customer
    #     c = LT_CUSTOMERS.iloc[[LTi]]
    #     next_VC = VC + c['DEMAND'].values[0]
    #
    #     # customers param values
    #     RT = c['READY TIME'].values[0]
    #     DT = c['DUE DATE'].values[0]
    #     ST = c['SERVICE TIME'].values[0]
    #
    #     for ri in range(0, len(route)):
    #         r = route.iloc[[ri]]
    #         next_VC = VC + c['DEMAND'].values[0]
    #
    #         # customers param values
    #         RT = c['READY TIME'].values[0]
    #         DT = c['DUE DATE'].values[0]
    #         ST = c['SERVICE TIME'].values[0]
    #
    #     if next_VC > vehicle_capacity or TT > DT:
    #        continue
    #
    #     if TT <= RT:
    #        TT = RT
    #
    #     TT += ST
    #     VC = next_VC
    #
    #     # place customer at route
    #     route = pd.concat([route, c], ignore_index=False, axis=0)






        # print(TT)
        # TT = TT if TT <= RT else RT
        # TT = TT + c['SERVICE TIME'].values[0]
        # print( TT + c['SERVICE TIME'].values[0])
        # TT += c['SERVICE TIME'].values[0]

        # RT = c['READY TIME'].values[0]
        # TT = TT if TT <= RT else RT
        # TT += c['SERVICE TIME']

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
