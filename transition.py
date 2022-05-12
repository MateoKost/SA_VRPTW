from random import randrange
from Preliminaries import *
from random import uniform
import pandas as pd


def transition(routes, CUSTOMERS, radius, cnumber):

    # cannot operate directly on previous solution & radius value
    localRadius = 0 + radius
    new_routes = routes.copy()

    # initialize clients to remove df
    clientsToRemove = pd.DataFrame(columns=CUSTOMERS.columns, index=CUSTOMERS.index)
    clientsToRemove = clientsToRemove.dropna()

    # get random not empty route
    randomRoute = findRandomNotEmptyRoute(new_routes)

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
        # enforceIntoRandomRoute(clientsToRemove, new_routes)

        # multiply radius
        localRadius *= RADIUS_SCALAR

        print(f'removedCounter - {removedCounter}')

    print(f'N routes - {len(new_routes)}')

    return new_routes


def findRandomRoute(routes):
    randomRouteIndex = randrange(len(routes))
    return routes[randomRouteIndex]


def findRandomNotEmptyRoute(routes):
    randomRoute = findRandomRoute(routes)
    while len(randomRoute) <= 0:
        randomRoute = findRandomRoute(routes)
    return randomRoute


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
    for cr in range(0, len(clientsToReplace)):
        cr_row = clientsToReplace.iloc[[cr]]
        randomRoute = findRandomRoute(routes)


def removeEmptyRoutes(routes):
    new_routes = routes.copy()

    new_routes.sort(key=lambda x: len(x.index), reverse=True)

    while len(new_routes[-1].index) == 0:
        del new_routes[-1]

    return new_routes

