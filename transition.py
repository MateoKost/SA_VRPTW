from random import randrange
from Preliminaries import *
from random import uniform
import pandas as pd


def transition(routes, CUSTOMERS, radius):
    # initialize clients to remove df
    clientsToRemove = pd.DataFrame(columns=CUSTOMERS.columns, index=CUSTOMERS.index)
    clientsToRemove = clientsToRemove.dropna()

    # get random route
    randomRouteIndex = randrange(len(routes))
    randomRoute = routes[randomRouteIndex]

    # get random customer and his coords
    randomCustomerIndex = randrange(len(randomRoute))
    randomCustomer = randomRoute.iloc[[randomCustomerIndex]]
    randomCustomer_x = randomCustomer['XCOORD.'].values[0]
    randomCustomer_y = randomCustomer['YCOORD.'].values[0]
    clientsToRemove = pd.concat([clientsToRemove, randomCustomer], ignore_index=False, axis=0)

    # apply method of increasing radius
    for i in range(0, len(CUSTOMERS)):
        customer_i = CUSTOMERS.iloc[[i]]
        x_i = customer_i['XCOORD.'].values[0]
        y_i = customer_i['YCOORD.'].values[0]

        if containsInRadius(x_i, y_i, randomCustomer_x, randomCustomer_y, radius):
            if uniform(0, 1) <= PROPABILITY_CNUMBER:
                clientsToRemove = pd.concat([clientsToRemove, customer_i], ignore_index=False, axis=0)

    return routes


def containsInRadius(x, y, a, b, r):
    return pow((x - a), 2) + pow((y - b), 2) <= pow(r, 2)
