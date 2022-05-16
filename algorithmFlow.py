import copy
from Preliminaries import *
import math
import pandas as pd
import initialSolution
from transition import transition, upgradeRoutes
from random import uniform
from statistics import median
from benchmarkReader import appendEpochResult, generateBenchmarkRunName, writeEpochResult, readInitialSolution
import re


def run(exportDirectory, benchmark, fdata, vehicle_capacity, importInitialSolution, initialsDirectoryPath):
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

    if importInitialSolution:
        routes = importInitial(f'{initialsDirectoryPath}{benchmark}', EE_CUSTOMERS, depot)
    else:
        # sort customers by windows
        EE_CUSTOMERS = EE_CUSTOMERS.sort_values(by=['WINDOW_LENGTH', 'READY TIME', 'DUE DATE'],
                                                ascending=[True, True, True])

        # mt/lt customers
        MT_CUSTOMERS = EE_CUSTOMERS.head(MT_CLIENT_C1)
        LT_CUSTOMERS = EE_CUSTOMERS.tail(LT_CLIENT_C1)

        # retrieve Everyone Else
        EE_CUSTOMERS.drop(MT_CUSTOMERS.index, axis=0, inplace=True)
        EE_CUSTOMERS.drop(LT_CUSTOMERS.index, axis=0, inplace=True)

        # get initial solution
        routes = initialSolution.flow(MT_CUSTOMERS, LT_CUSTOMERS, EE_CUSTOMERS, vehicle_capacity)

        # try to upgrade the solution
        routes = upgradeRoutes(routes, UPGRADE_ATTEMPTS, vehicle_capacity)

    # sum distances
    distances = 0
    for i in range(0, len(routes)):
        distances += totalRouteDistance(pd.concat([depot, routes[i], depot], ignore_index=False, axis=0))

    runName = generateBenchmarkRunName(benchmark, TZERO, vehicle_capacity)
    # append col names
    appendEpochResult(exportDirectory, runName, 'solutions.csv', [[]], header=True)
    formattedResult = [[runName, 0, TZERO, distances, len(routes)]]
    # append initial solution
    appendEpochResult(exportDirectory, runName, 'solutions.csv', formattedResult, header=False)
    # export initial solution
    writeEpochResult(exportDirectory, runName, 0, TZERO, routes, 'epoch')

    # append best ever solutions
    appendEpochResult(exportDirectory, runName, 'best-ever-solutions.csv', [[]], header=True)
    formattedResult = [[runName, 0, TZERO, distances, len(routes)]]
    appendEpochResult(exportDirectory, runName, 'best-ever-solutions.csv', formattedResult, header=False)
    # export best ever solution
    writeEpochResult(exportDirectory, runName, 0, TZERO, routes, 'be_epoch')

    best_solution, best_distances = annealing(exportDirectory, runName, routes, distances, fdata, depot,
                                              vehicle_capacity)

    return best_distances, len(best_solution)


def annealing(exportDirectory, runName, routes, distances, CUSTOMERS, depot, VEHICLE_CAPACITY):
    temperature = TZERO
    # about 10-15% of customers number
    cnumber = PROPORTION_CNUMBER * len(CUSTOMERS)
    # about 25% of median of distances between customers
    radius = 0.25 * distanceMedian(CUSTOMERS)
    best_solution = copy.deepcopy(routes)
    best_distances = distances
    best_ever_solution = copy.deepcopy(routes)
    best_ever_distances = distances

    for epoch in range(1, EPOCH + 1):
        print(f'epoch - {epoch}')
        for iteration in range(1, ITER + 1):
            step_solution = transition(best_solution, CUSTOMERS, radius, cnumber, VEHICLE_CAPACITY)
            # sum distances
            step_distances = 0
            for i in range(0, len(step_solution)):
                step_distances += totalRouteDistance(pd.concat([depot, step_solution[i], depot],
                                                               ignore_index=False, axis=0))
            delta = objectiveFunction(len(step_solution), step_distances) - objectiveFunction(len(best_solution),
                                                                                              best_distances)
            # change best solution
            if delta < 0:
                best_solution = step_solution
                best_distances = step_distances
            if step_distances <= best_ever_distances:
                best_ever_solution = step_solution
                best_ever_distances = step_distances
            else:
                b = uniform(0, 1)
                if b < math.exp(-delta / temperature):
                    best_solution = step_solution
                    best_distances = step_distances

        # append best solution
        formattedResult = [[runName, epoch, temperature, best_distances, len(best_solution)]]
        appendEpochResult(exportDirectory, runName, 'solutions.csv', formattedResult, header=False)
        # export initial solution
        writeEpochResult(exportDirectory, runName, epoch, temperature, best_solution, 'epoch')

        # append best ever solutions
        formattedResult = [[runName, epoch, temperature, best_ever_distances, len(best_ever_solution)]]
        appendEpochResult(exportDirectory, runName, 'best-ever-solutions.csv', formattedResult, header=False)
        # export best ever solution
        writeEpochResult(exportDirectory, runName, epoch, temperature, best_ever_solution, 'be_epoch')

        # decrease annealing temperature
        temperature = decreaseTemperatureFunction(temperature)

    return best_solution, best_distances


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def totalRouteDistance(route):
    d = 0
    for i in range(1, len(route)):
        customerPrevious = route.iloc[[i - 1]]
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


def importInitial(source, CUSTOMERS, depot):
    df = readInitialSolution(source)

    list_of_char = ['\\[', '\\]', ' ']
    pattern = '[' + ''.join(list_of_char) + ']'

    routes = []

    for ri in df.index:
        routeRow = df.loc[ri]
        customersString = re.sub(pattern, '', routeRow.customers).split(',')

        route = pd.DataFrame(columns=CUSTOMERS.columns, index=CUSTOMERS.index)
        route = route.dropna()

        for cs in customersString:
            customer = CUSTOMERS.loc[[int(cs)]]
            route = pd.concat([route, customer], ignore_index=False, axis=0)

        routes.append(route)

    # sum distances
    distances = 0
    for i in range(0, len(routes)):
        distances += totalRouteDistance(pd.concat([depot, routes[i], depot], ignore_index=False, axis=0))

    print(distances)

    return routes
