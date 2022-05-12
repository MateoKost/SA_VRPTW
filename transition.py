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
    randomRouteIndex = randrange(len(new_routes))
    randomRoute = new_routes[randomRouteIndex]
    while len(randomRoute) <= 0:
        randomRouteIndex = randrange(len(new_routes))
        randomRoute = new_routes[randomRouteIndex]

    # get random customer and his coords
    randomCustomerIndex = randrange(len(randomRoute))
    randomCustomer = randomRoute.iloc[[randomCustomerIndex]]
    randomCustomer_x = randomCustomer['XCOORD.'].values[0]
    randomCustomer_y = randomCustomer['YCOORD.'].values[0]
    removedCounter = 1

    # remove randomCustomer from route
    randomRoute.drop(randomCustomer.index, axis=0, inplace=True)

    # consider putting this into separate function
    # get second random not empty route
    # randomRouteIndex = randrange(len(new_routes))
    # secondRandomRoute = new_routes[randomRouteIndex]
    # while len(secondRandomRoute) <= 0:
    #     randomRouteIndex = randrange(len(new_routes))
    #     secondRandomRoute = new_routes[randomRouteIndex]

    # loop for reaching clientsToRemove length equals cnumber

    while removedCounter < cnumber:

        # apply method of increasing radius
        for ri in range(0, len(new_routes)):
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

            if removedCounter >= cnumber:
                break

        removeClientsFromRoutes(new_routes, clientsToRemove)
        # print(clientsToRemove)

        # if removedCounter == 1:
        localRadius *= RADIUS_SCALAR

        print(f'removedCounter - {removedCounter}')

    return new_routes


def containsInRadius(x, y, a, b, r):
    return pow((x - a), 2) + pow((y - b), 2) <= pow(r, 2)


def searchReplacement(route, customer):
    print(searchReplacement)


def removeClientsFromRoutes(routes, clientsToRemove):

    itRoutesCopy = routes.copy()

    for ri in range(0, len(itRoutesCopy)):
        route = itRoutesCopy[ri]

        # localToRemove = []
        localToRemove = pd.DataFrame(columns=clientsToRemove.columns, index=clientsToRemove.index)
        localToRemove = localToRemove.dropna()

        for cr in range(0, len(clientsToRemove)):
            # print(f'cr - {clientsToRemove.iloc[[cr]].index.values[0]}')

            cr_row = clientsToRemove.iloc[[cr]]
            cr_index = cr_row.index
            cr_index_v = cr_index.values[0]
            # print(cr_index in route.index)
            # if cr_index in route.index:
            #     localToRemove.append(cr_index)
            if cr_index_v in route.index.values.tolist():
                # print(routes[ri])
                localToRemove = pd.concat([localToRemove, cr_row], ignore_index=False, axis=0)
                # print(cr_index_v)
                # routes[ri].drop(cr_index, axis=0, inplace=True)

                # routes[ri].drop(cr_index, axis=0, inplace=True)

                # clientsToRemove.drop(cr_index, axis=0, inplace=True)
                # print(routes[ri])
                # print('clientsToRemove')
                # print(clientsToRemove)

                # localToRemove.append(cr_index)

        # print(pd.DataFrame(data=localToRemove))
        # print(localToRemove)
        # print(localToRemove.index)
        # print(routes[ri])
        print(localToRemove)
        routes[ri].drop(localToRemove.index, axis=0, inplace=True)
        clientsToRemove.drop(localToRemove.index, axis=0, inplace=True)
        # print(clientsToRemove)

        # route = pd.DataFrame(columns=MT_CUSTOMERS.columns, index=MT_CUSTOMERS.index)
        # route = route.dropna()


            # if routecr.index
        # for cr in route
        #     if routecr.index
        # route.drop(clientsToRemove.index, axis=0, inplace=True)
        # for ci in range(0, len(route)):
