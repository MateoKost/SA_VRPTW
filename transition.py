from random import randrange
from Preliminaries import *
from random import uniform
from initialSolution import assignLT_CUSTOMERS, assignMT_CUSTOMERS
import pandas as pd
import copy


def transition(routes, CUSTOMERS, radius, cnumber, vehicle_capacity):
    # cannot operate directly on previous solution & radius value
    localRadius = 0 + radius
    # deep copy is required
    new_routes = copy.deepcopy(routes)

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
        clientsForcedToLeave = enforceIntoRandomRoute(clientsToRemove, new_routes, vehicle_capacity)

        # drop clientsToRemove
        clientsToRemove.drop(clientsToRemove.index, axis=0, inplace=True)

        # increment counter
        removedCounter += len(clientsForcedToLeave)

        # assign clientsForcedToLeave into existing routes
        n = len(new_routes)
        for ri in range(0, n):
            route, clientsForcedToLeave = assignLT_CUSTOMERS(new_routes[ri], clientsForcedToLeave, vehicle_capacity)
            new_routes[ri] = route

        # assign remaining clientsForcedToLeave into new routes the way MT_CUSTOMERS were assigned
        if len(clientsForcedToLeave) > 0:
            while len(clientsForcedToLeave) > 0:
                route, clientsForcedToLeave = assignMT_CUSTOMERS(clientsForcedToLeave, vehicle_capacity)
                new_routes.append(route)

        # multiply radius
        localRadius *= RADIUS_SCALAR

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
    itRoutesCopy = copy.deepcopy(routes)

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


def enforceIntoRandomRoute(clientsToReplace, routes, vehicle_capacity):
    # container for customers enforced to leave their routes
    forcedToLeaveContainer = pd.DataFrame(columns=clientsToReplace.columns, index=clientsToReplace.index)
    forcedToLeaveContainer = forcedToLeaveContainer.dropna()

    # iterate over clientsToReplace
    for cr in range(0, len(clientsToReplace)):
        cr_row = clientsToReplace.iloc[[cr]]

        randomRoute, randomRouteIndex = findRandomRoute(routes)

        newRoute,clientsToLeave = findNewPlace(cr_row, randomRoute, vehicle_capacity)

        routes[randomRouteIndex] = newRoute
        forcedToLeaveContainer = pd.concat([forcedToLeaveContainer, clientsToLeave], ignore_index=False, axis=0)

    return forcedToLeaveContainer


def removeEmptyRoutes(routes):
    new_routes = copy.deepcopy(routes)

    new_routes.sort(key=lambda x: len(x.index), reverse=True)

    while len(new_routes[-1].index) == 0:
        del new_routes[-1]

    return new_routes


def findNewPlace(customer, route, vehicle_capacity):
    # define new route with only the customer inside
    newRoute = pd.DataFrame(columns=route.columns, index=route.index)
    newRoute = newRoute.dropna()
    newRoute = pd.concat([newRoute, customer], ignore_index=False, axis=0)

    # place customers from the route into the new route
    newRoute, clientsToLeave = assignLT_CUSTOMERS(newRoute, route, vehicle_capacity)
    previousCTLength = len(clientsToLeave)

    while len(clientsToLeave) > 0:
        newRoute, clientsToLeave = assignLT_CUSTOMERS(newRoute, clientsToLeave, vehicle_capacity)
        if previousCTLength == len(clientsToLeave):
            break
        previousCTLength = len(clientsToLeave)

    # the customers which haven't been placed are new clients to replace
    return newRoute, clientsToLeave
