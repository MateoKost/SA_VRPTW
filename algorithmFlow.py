from Preliminaries import *
import utils
import math
import pandas as pd
import initialSolution
from transition import transition
from random import uniform
from statistics import median


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
    routes = initialSolution.flow(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, VEHICLE_CAPACITY)

    # sum distances
    distances = 0
    for i in range(0, len(routes)):
        distances += totalRouteDistance(pd.concat([depot, routes[i]], ignore_index=False, axis=0))

    print('initial solution')
    print(f'total distance - {distances}')
    print(f'vehicles - {len(routes)}')

    best_solution, best_distances = annealing(routes, distances, fdata, depot)

    return best_distances, len(best_solution)


def annealing(routes, distances, CUSTOMERS, depot):
    temperature = TZERO
    # about 10-15% of customers number
    cnumber = PROPORTION_CNUMBER * len(CUSTOMERS)
    # about 25% of median of distances between customers
    radius = 0.25 * distanceMedian(CUSTOMERS)
    best_solution = routes.copy()
    best_distances = distances
    best_ever_solution = routes.copy()
    best_ever_distances = distances
    for epoch in range(1, 33):
        print(f'epoch - {epoch}')
        for iteration in range(1, 200):
            step_solution = transition(best_solution, CUSTOMERS, radius, cnumber)
            # sum distances
            step_distances = 0
            for i in range(0, len(step_solution)):
                step_distances += totalRouteDistance(pd.concat([depot, step_solution[i]], ignore_index=False, axis=0))
            delta = step_distances - best_distances
            # change best solution
            if delta < 0:
                best_solution = step_solution
                best_distances = step_distances
            if step_distances <= best_ever_distances:
                best_ever_solution = step_solution
                best_ever_distances = step_distances
            else:
                b = uniform(0, 1)
                if b < math.exp(-delta/temperature):
                    best_solution = step_solution
                    best_distances = step_distances
        decreaseTemperatureFunction(temperature)
        print(f'\tN CUSTOMERS on best_solution - {sum(len(x) for x in best_solution)}')
        print(f'\tbest_distances - {best_distances}')
        print(f'\tN routes - {len(best_solution)}')
        print(f'\tbest_ever_solution - {best_ever_solution}')
        print(f'\tbest_ever_distances - {best_ever_distances}')
        print(f'\tN routes - {len(best_ever_solution)}')
    print(f'END - {len(best_solution)}')
    print(f'N CUSTOMERS on best_solution - {sum(len(x) for x in best_solution)}')
    print(f'best_distances - {best_distances}')
    print(f'N routes - {len(best_solution)}')
    return best_solution, best_distances


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def totalRouteDistance(route):
    d = 0
    for i in range(1, len(route)):
        customerPrevious = route.iloc[[i-1]]
        x1 = customerPrevious['XCOORD.'].values[0]
        y1 = customerPrevious['YCOORD.'].values[0]

        customerAtTourMoment = route.iloc[[i]]
        x2 = customerAtTourMoment['XCOORD.'].values[0]
        y2 = customerAtTourMoment['YCOORD.'].values[0]

        d = d + distance(x1, y1, x2, y2)
    return d


def distanceMedian(CUSTOMERS):
    distances = []
    for i in range(0, len(CUSTOMERS)):
        customer_i = CUSTOMERS.iloc[[i]]
        x_i = customer_i['XCOORD.'].values[0]
        y_i = customer_i['YCOORD.'].values[0]
        for j in range(0, len(CUSTOMERS)):
            customer_j = CUSTOMERS.iloc[[j]]
            x_j = customer_j['XCOORD.'].values[0]
            y_j = customer_j['YCOORD.'].values[0]
            distances.append(distance(x_i, y_i, x_j, y_j))
    return median(distances)
