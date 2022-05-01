import pandas as pd


def flow(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, VEHICLE_CAPACITY):

    # print(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, VEHICLE_CAPACITY)

    # initialize routes
    routes = []
    route, MT_CUSTOMERS = assignMT_CUSTOMERS(MT_CUSTOMERS, VEHICLE_CAPACITY)

def assignMT_CUSTOMERS(MT_CUSTOMERS, VEHICLE_CAPACITY):
    # specify new vehicle route
    route = pd.DataFrame(columns=MT_CUSTOMERS.columns, index=MT_CUSTOMERS.index)
    route = route.dropna()

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
        if next_VC > VEHICLE_CAPACITY or TT > DT:
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

    return route, MT_CUSTOMERS
