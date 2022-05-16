import pandas as pd
import benchmarkReader
import re
# from algorithmFlow import


def flow(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, VEHICLE_CAPACITY):
    # initialize routes
    routes = []

    # assign MT_CUSTOMERS to new routes
    while len(MT_CUSTOMERS) > 0:
        route, MT_CUSTOMERS = assignMT_CUSTOMERS(MT_CUSTOMERS, VEHICLE_CAPACITY)
        routes.append(route)

    # assign LT_CUSTOMERS into existing routes
    for ri in range(0, len(routes)):
        route, LT_CUSTOMERS = assignLT_CUSTOMERS(routes[ri], LT_CUSTOMERS, VEHICLE_CAPACITY)
        routes[ri] = route

    # assign remaining LT_CUSTOMERS into new routes the way MT_CUSTOMERS were assigned
    if len(LT_CUSTOMERS) > 0:
        while len(LT_CUSTOMERS) > 0:
            route, LT_CUSTOMERS = assignMT_CUSTOMERS(LT_CUSTOMERS, VEHICLE_CAPACITY)
            routes.append(route)

    # assign EE_CUSTOMERS into existing routes
    for ri in range(0, len(routes)):
        route, EE_CUSTOMERS = assignLT_CUSTOMERS(routes[ri], EE_CUSTOMERS, VEHICLE_CAPACITY)
        routes[ri] = route

    # assign remaining EE_CUSTOMERS into new routes the way MT_CUSTOMERS were assigned
    if len(EE_CUSTOMERS) > 0:
        while len(EE_CUSTOMERS) > 0:
            route, EE_CUSTOMERS = assignMT_CUSTOMERS(EE_CUSTOMERS, VEHICLE_CAPACITY)
            routes.append(route)

    return routes


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


def assignLT_CUSTOMERS(route, LT_CUSTOMERS, VEHICLE_CAPACITY):

    # cannot modify a dataframe while it's being iterated
    LT_CUSTOMERS_copy = LT_CUSTOMERS.copy()

    # iterate over LTs
    for LTi in range(0, len(LT_CUSTOMERS)):

        # Total Time
        TT = 0
        # Vehicle Capacity
        VC = 0

        # get i-th customer
        c = LT_CUSTOMERS.iloc[[LTi]]

        # customers param values
        LTi_D = c['DEMAND'].values[0]
        LTi_RT = c['READY TIME'].values[0]
        LTi_DT = c['DUE DATE'].values[0]
        LTi_ST = c['SERVICE TIME'].values[0]

        # check capacity available
        route_capacity = 0
        for ri in range(0, len(route)):
            r = route.iloc[[ri]]
            route_capacity += r['DEMAND'].values[0]

        # when vehicle has available space for customer demand
        if route_capacity + LTi_D <= VEHICLE_CAPACITY:

            # check possibility of placing lt customer at the beginning of route
            if len(route) > 0:
                r = route.iloc[[0]]
                r_D = r['DEMAND'].values[0]
                r_RT = r['READY TIME'].values[0]
                r_DT = r['DUE DATE'].values[0]
                r_ST = r['SERVICE TIME'].values[0]

                prev_availableTime = TT

                if prev_availableTime <= LTi_RT:
                    prev_availableTime = LTi_RT

                prev_availableTime += LTi_ST

                if prev_availableTime <= r_DT:
                    route = pd.concat([c, route], ignore_index=False, axis=0)
                    LT_CUSTOMERS_copy.drop(c.index, axis=0, inplace=True)
                    # TT = prev_availableTime
                    break

            # check possibility of placing lt customer at the end of route
            if len(route) > 0:
                r = route.iloc[[len(route) - 1]]
                # r_D = r['DEMAND'].values[0]
                r_RT = r['READY TIME'].values[0]
                r_DT = r['DUE DATE'].values[0]
                r_ST = r['SERVICE TIME'].values[0]

                if r_RT + r_ST <= LTi_DT:
                    route = pd.concat([route, c], ignore_index=False, axis=0)
                    LT_CUSTOMERS_copy.drop(c.index, axis=0, inplace=True)
                    break

            # find available place at route between existing customers
            for ri in range(0, len(route)-1):

                # current customer at route
                r_a = route.iloc[[ri]]
                r_a_RT = r_a['READY TIME'].values[0]
                r_a_ST = r_a['SERVICE TIME'].values[0]

                # update the time
                prev_availableTime = TT
                if prev_availableTime <= r_a_RT:
                    prev_availableTime = r_a_RT
                prev_availableTime += r_a_ST

                # next customer at route
                r_b = route.iloc[[ri + 1]]
                r_b_DT = r_b['DUE DATE'].values[0]

                # check whether existing time windows wouldn't be violated
                between_available_time = prev_availableTime
                if between_available_time <= LTi_RT:
                    between_available_time = LTi_RT
                between_available_time += LTi_ST

                if between_available_time <= r_b_DT:
                    route = pd.concat([route.iloc[:ri+1], c, route.iloc[ri+1:]], ignore_index=False, axis=0)
                    LT_CUSTOMERS_copy.drop(c.index, axis=0, inplace=True)
                    break

                # increment time
                TT = prev_availableTime

        else:
            break

    return route, LT_CUSTOMERS_copy


