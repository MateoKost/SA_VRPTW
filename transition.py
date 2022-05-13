from random import randrange
from Preliminaries import *
from random import uniform
from initialSolution import assignLT_CUSTOMERS
import pandas as pd


def transition(routes, CUSTOMERS, radius, cnumber):
    # cannot operate directly on previous solution & radius value
    localRadius = 0 + radius
    new_routes = routes.copy()

    # initialize clients to remove df
    clientsToRemove = pd.DataFrame(columns=CUSTOMERS.columns, index=CUSTOMERS.index)
    clientsToRemove = clientsToRemove.dropna()

    # get random not empty route
    randomRoute, randomRouteIndex = findRandomNotEmptyRoute(new_routes)

    # get random customer and his coords
    randomCustomerIndex = randrange(len(randomRoute))
    randomCustomer = randomRoute.iloc[[randomCustomerIndex]]
    randomCustomer_x = randomCustomer['XCOORD.'].values[0]
    randomCustomer_y = randomCustomer['YCOORD.'].values[0]
    clientsToRemove = pd.concat([clientsToRemove, randomCustomer], ignore_index=False, axis=0)
    removedCounter = 1

    # # remove randomCustomer from route
    # randomRoute.drop(randomCustomer.index, axis=0, inplace=True)

    # loop for reaching cnumber
    while removedCounter < cnumber:

        # apply method of increasing radius
        for ri in range(0, len(new_routes)):
            if removedCounter >= cnumber:
                break

            route = new_routes[ri]

            for i in range(0, len(route)):
                customer_i = route.iloc[[i]]
                x_i = customer_i['XCOORD.'].values[0]
                y_i = customer_i['YCOORD.'].values[0]

                if customer_i.index == randomCustomer.index:
                    continue

                if containsInRadius(x_i, y_i, randomCustomer_x, randomCustomer_y, localRadius):
                    if uniform(0, 1) <= PROPABILITY_CNUMBER:
                        clientsToRemove = pd.concat([clientsToRemove, customer_i], ignore_index=False, axis=0)
                        removedCounter += 1

        # remove clientsToRemove from new_routes
        removeClientsFromRoutes(new_routes, clientsToRemove)

        # remove empty routes
        new_routes = removeEmptyRoutes(new_routes)

        # force new client positions in random routes
        clientsForcedToLeave = enforceIntoRandomRoute(clientsToRemove, new_routes)
        removedCounter += len(clientsForcedToLeave)

        # multiply radius
        localRadius *= RADIUS_SCALAR

        print(f'removedCounter - {removedCounter}')

    print(f'N routes - {len(new_routes)}')
    # print(new_routes)

    print(sum(len(x) for x in new_routes))

    return new_routes


def findRandomRoute(routes):
    randomRouteIndex = randrange(len(routes))
    return routes[randomRouteIndex], randomRouteIndex


def findRandomNotEmptyRoute(routes):
    randomRoute, randomRouteIndex = findRandomRoute(routes)
    while len(randomRoute) <= 0:
        randomRoute, randomRouteIndex = findRandomRoute(routes)
    return randomRoute, randomRouteIndex


def containsInRadius(x, y, a, b, r):
    return pow((x - a), 2) + pow((y - b), 2) <= pow(r, 2)


def searchReplacement(route, customer):
    print(searchReplacement)


def removeClientsFromRoutes(routes, clientsToRemove):
    itRoutesCopy = routes.copy()

    for ri in range(0, len(itRoutesCopy)):
        route = itRoutesCopy[ri]

        localToRemove = pd.DataFrame(columns=clientsToRemove.columns, index=clientsToRemove.index)
        localToRemove = localToRemove.dropna()

        for cr in range(0, len(clientsToRemove)):
            cr_row = clientsToRemove.iloc[[cr]]
            cr_index = cr_row.index
            cr_index_v = cr_index.values[0]
            if cr_index_v in route.index.values.tolist():
                localToRemove = pd.concat([localToRemove, cr_row], ignore_index=False, axis=0)

        routes[ri].drop(localToRemove.index, axis=0, inplace=True)
        # clientsToRemove.drop(localToRemove.index, axis=0, inplace=True)


def enforceIntoRandomRoute(clientsToReplace, routes):
    # container for customers enforced to leave their routes
    forcedToLeaveContainer = pd.DataFrame(columns=clientsToReplace.columns, index=clientsToReplace.index)
    forcedToLeaveContainer = forcedToLeaveContainer.dropna()

    # iterate over clientsToReplace
    for cr in range(0, len(clientsToReplace)):
        cr_row = clientsToReplace.iloc[[cr]]
        randomRoute, randomRouteIndex = findRandomRoute(routes)
        newRoute, clientsToLeave = findNewPlace(cr_row, randomRoute)
        routes[randomRouteIndex] = newRoute
        forcedToLeaveContainer = pd.concat([forcedToLeaveContainer, clientsToLeave], ignore_index=False, axis=0)

    return forcedToLeaveContainer


def removeEmptyRoutes(routes):
    new_routes = routes.copy()

    new_routes.sort(key=lambda x: len(x.index), reverse=True)

    while len(new_routes[-1].index) == 0:
        del new_routes[-1]

    return new_routes


def findNewPlace(customer, route):
    # define new route
    newRoute = pd.DataFrame(columns=route.columns, index=route.index)
    newRoute = newRoute.dropna()
    newRoute = pd.concat([newRoute, customer], ignore_index=False, axis=0)

    newRoute, clientsToLeave = assignLT_CUSTOMERS(newRoute, route, VEHICLE_CAPACITY_C1)
    return newRoute, clientsToLeave



    # # Total Time
    # TT = 0
    # # Vehicle Capacity
    # VC = 0
    #
    # # customers param values
    # RT_C = customer['READY TIME'].values[0]
    # DT_C = customer['DUE DATE'].values[0]
    # ST_C = customer['SERVICE TIME'].values[0]
    # D_C = customer['DEMAND'].values[0]
    #
    # # define new route
    # newRoute = pd.DataFrame(columns=route.columns, index=route.index)
    # newRoute = route.dropna()
    #
    # # define customers to leave df
    # customersToLeave = pd.DataFrame(columns=route.columns, index=route.index)
    # customersToLeave = route.dropna()
    #
    # # check if it's available to place customer without enforcing
    # # check capacity available
    # route_capacity = 0
    # for ri in range(0, len(route)):
    #     r = route.iloc[[ri]]
    #     route_capacity += r['DEMAND'].values[0]
    #
    # # when vehicle has available space for customer demand
    # if route_capacity + D_C <= VEHICLE_CAPACITY_C1:  # !!! param
    #
    #     # check possibility of placing lt customer at the beginning of route
    #     if len(route) > 0:
    #         r = route.iloc[[0]]
    #         r_D = r['DEMAND'].values[0]
    #         r_RT = r['READY TIME'].values[0]
    #         r_DT = r['DUE DATE'].values[0]
    #         r_ST = r['SERVICE TIME'].values[0]
    #
    #         prev_availableTime = TT
    #
    #         if prev_availableTime <= RT_C:
    #             prev_availableTime = RT_C
    #
    #         prev_availableTime += RT_C
    #
    #         if prev_availableTime <= r_DT:
    #             newRoute = pd.concat([customer, route], ignore_index=False, axis=0)
    #             return True, newRoute
    #
    #     # check possibility of placing lt customer at the end of route
    #     if len(route) > 0:
    #         r = route.iloc[[len(route) - 1]]
    #         # r_D = r['DEMAND'].values[0]
    #         r_RT = r['READY TIME'].values[0]
    #         r_DT = r['DUE DATE'].values[0]
    #         r_ST = r['SERVICE TIME'].values[0]
    #
    #         if r_RT + r_ST <= DT_C:
    #             newRoute = pd.concat([route, customer], ignore_index=False, axis=0)
    #             return True, newRoute
    #
    #     # find available place at route between existing customers
    #     for ri in range(0, len(route) - 1):
    #
    #         # current customer at route
    #         r_a = route.iloc[[ri]]
    #         r_a_RT = r_a['READY TIME'].values[0]
    #         r_a_ST = r_a['SERVICE TIME'].values[0]
    #
    #         # update the time
    #         prev_availableTime = TT
    #         if prev_availableTime <= r_a_RT:
    #             prev_availableTime = r_a_RT
    #         prev_availableTime += r_a_ST
    #
    #         # next customer at route
    #         r_b = route.iloc[[ri + 1]]
    #         r_b_DT = r_b['DUE DATE'].values[0]
    #
    #         # check whether existing time windows wouldn't be violated
    #         between_available_time = prev_availableTime
    #         if between_available_time <= RT_C:
    #             between_available_time = RT_C
    #         between_available_time += ST_C
    #
    #         if between_available_time <= r_b_DT:
    #             newRoute = pd.concat([route.iloc[:ri + 1], customer, route.iloc[ri + 1:]], ignore_index=False, axis=0)
    #             return True, newRoute
    #
    #         # increment time
    #         TT = prev_availableTime
    #
    #

    # # else enforce bothering customers to leave
    # TT = 0
    # VC = 0
    # customerPlaced = False
    # for ri in range(0, len(route)):
    #
    #         # current customer at route
    #         r_a = route.iloc[[ri]]
    #         r_a_RT = r_a['READY TIME'].values[0]
    #         r_a_ST = r_a['SERVICE TIME'].values[0]
    #         r_a_D = r_a['DEMAND'].values[0]
    #
    #         next_VC_a = VC + r_a_D
    #         next_VC_C = VC + D_C
    #
    #         # update the local time
    #         advancedTime = TT
    #
    #         # check if vehicle capacity with current customer demand is available or DUE DATE isn't reached
    #         # if not skip to next customer
    #         if next_VC_a > VEHICLE_CAPACITY_C1 or TT > DT_C:
    #             continue
    #
    #         # (optional) update total time by RT
    #         if TT <= RT:
    #             TT = RT
    #
    #         # increment total time by customer service time
    #         TT += ST
    #         # increment vehicle capacity
    #         VC = next_VC
    #
    #
    #         if customerPlaced:
    #             continue
    #
    #         # place customer into route
    #         newRoute = pd.concat([newRoute, customer], ignore_index=False, axis=0)
    #         customerPlaced = True
    #
    #         customersToLeave = pd.concat([customersToLeave, r_a], ignore_index=False, axis=0)
    #
    #
    #
    #         # if prev_availableTime <= r_a_RT:
    #         #     prev_availableTime = r_a_RT
    #         # prev_availableTime += r_a_ST
    #
    #         # # next customer at route
    #         # r_b = route.iloc[[ri + 1]]
    #         # r_b_DT = r_b['DUE DATE'].values[0]
    #         #
    #         # # check whether existing time windows wouldn't be violated
    #         # between_available_time = prev_availableTime
    #         # if between_available_time <= RT_C:
    #         #     between_available_time = RT_C
    #         # between_available_time += ST_C
    #
    #         # if between_available_time <= r_b_DT:
    #         #     newRoute = pd.concat([route.iloc[:ri + 1], customer, route.iloc[ri + 1:]], ignore_index=False, axis=0)
    #         #     return True, newRoute
    #
    #         # increment time
    #         TT = advancedTime


    # return - whether customer has been placed into the route,
    # whether enforced replacement happened and return customers which had to leave
    return True, newRoute, True, customersToLeave







    #
    #
    # # iterate over route
    # for ci in range(0, len(route)):
    #     # get i-th customer
    #     c = route.iloc[[ci]]
    #     next_VC = VC + c['DEMAND'].values[0]
    #
    #     # customers param values
    #     RT_i = c['READY TIME'].values[0]
    #     DT_i = c['DUE DATE'].values[0]
    #     ST_i = c['SERVICE TIME'].values[0]
    #

    # # check if vehicle capacity with current customer demand is available or DUE DATE isn't reached
    # # if not skip to next customer
    # if next_VC > VEHICLE_CAPACITY_C1 or TT > DT:
    #     continue
    #
    # # (optional) update total time by RT
    # if TT <= RT:
    #     TT = RT
    #
    # # increment total time by customer service time
    # TT += ST
    # # increment vehicle capacity
    # VC = next_VC
    #
    # # place customer at route
    # route = pd.concat([route, c], ignore_index=False, axis=0)

    # if()
    # route = newRoute
    # return True,
    #
    # return False
