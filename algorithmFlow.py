import copy
from Preliminaries import *
import math
import pandas as pd
import initialSolution
from transition import transition
from random import uniform, randrange
from statistics import median, mean
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
        routes = upgradeRoutes(routes, UPGRADE_ATTEMPTS, vehicle_capacity, depot, 5000)

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
            step_solution = upgradeRoutes2(step_solution, UPGRADE_ATTEMPTS, VEHICLE_CAPACITY, depot, best_distances)
            # sum distances
            step_distances = 0
            for i in range(0, len(step_solution)):
                step_distances += totalRouteDistance(pd.concat([depot, step_solution[i], depot],
                                                               ignore_index=False, axis=0))

            # localDelta = objectiveFunction(len(step_solution), step_distances) - objectiveFunction(len(best_solution),
            #                                                                                   best_distances)
            #
            # # print(localDelta)
            #
            # if localDelta < 0:
            #     best_solution = step_solution
            #     best_distances = step_distances

            # print(f'e-{epoch},  bd - {step_distances}, bed - {best_distances} ')

            delta = objectiveFunction(len(step_solution), step_distances) - objectiveFunction(len(best_solution),
                                                                                              best_distances)

            # delta = objectiveFunction(len(best_solution), best_distances) - objectiveFunction(len(best_ever_solution),
            #                                                                                   best_ever_distances)

                # change best solution
            if delta < 0:
                best_solution = step_solution
                best_distances = step_distances
               # best_ever_solution = best_solution
               # best_ever_distances = best_distances
                if step_distances <= best_ever_distances:
                    best_ever_solution = step_solution
                    best_ever_distances = step_distances
            else:
                b = uniform(0, 1)
                if b < math.exp(-delta / temperature):
                    best_solution = step_solution
                    best_distances = step_distances

            #     # change best solution
            # if delta < 0:
            #    best_ever_solution = best_solution
            #    best_ever_distances = best_distances
            #     # if step_distances <= best_ever_distances:
            #     #     best_ever_solution = step_solution
            #     #     best_ever_distances = step_distances
            # else:
            #     b = uniform(0, 1)
            #     if b < math.exp(-delta / temperature):
            #         best_ever_solution = best_solution
            #         best_ever_distances = best_distances

            print(f'e-{epoch}, it-{iteration}, bd - {step_distances}, bed - {best_distances} ')

            # print(f'e-{epoch}, it-{iteration}, bd - {best_distances}, bed - {best_ever_distances} ')

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


def upgradeRoutes(routes, upgradeAttempts, vehicle_capacity, depot, best_distances):

    new_routes = copy.deepcopy(routes)
    #
    distances = 0
    for i in range(0, len(routes)):
        distances += totalRouteDistance(pd.concat([depot, routes[i], depot],
                                                       ignore_index=False, axis=0))
    new_distances = distances

    # while new_distances > best_distances:

    for i in range(0, 25):

        # print(f'nd - {new_distances}  bd - {best_distances}')

    # for i in range(0, upgradeAttempts):
        new_routes.sort(key=lambda x: len(x.index))
        redumean = mean(totalRouteDistance(pd.concat([depot, x, depot], ignore_index=False, axis=0)) for x in new_routes)
        # redumean = mean(len(x) for x in new_routes)

        # routeToShift = []

        new_routes.sort(key=lambda x: totalRouteDistance(pd.concat([depot, x, depot], ignore_index=False, axis=0)))

        # for x in new_routes:
        #     print(totalRouteDistance(x))


        # new_routes = new_routes.assign(Percentage=lambda x: (x['Total_Marks'] / 500 * 100))

        # lambda x: print(x)

        #
        #
        #
        # print()

        # totalRouteDistance

        # randomRouteIndex = 0
        # routeToShift = new_routes[randomRouteIndex]
        # while totalRouteDistance(pd.concat([depot, routeToShift, depot], ignore_index=False, axis=0)) <= redumean:
        #     randomRouteIndex = randrange(len(new_routes))
        #     routeToShift = new_routes[randomRouteIndex]
        #     # print(f'{totalRouteDistance(routeToShift)}, {redumean}')
        # del new_routes[randomRouteIndex]

        # randomRouteIndex = randrange(len(new_routes))
        # routeToShift = new_routes[randomRouteIndex]
        # del new_routes[randomRouteIndex]

        routeToShift = new_routes[-1]
        del new_routes[-1]

        routeToShiftDistance = totalRouteDistance(pd.concat([depot, routeToShift, depot]))

        # for ri in range(0, len(new_routes)):
        #     route = new_routes[ri]
        #     if i % 2 == 1:
        #         if len(route) < redumean:
        #             routeToShift = route
        #             del new_routes[ri]
        #             break
        #     else:
        #         if len(route) > redumean:
        #             routeToShift = route
        #             del new_routes[ri]
        #             break



        # for ri in range(0, len(new_routes)):
        #     route = new_routes[ri]
        #     if i % 2 == 1:
        #         if len(route) < redumean:
        #             routeToShift = route
        #             del new_routes[ri]
        #             break
        #     else:
        #         if len(route) > redumean:
        #             routeToShift = route
        #             del new_routes[ri]
        #             break

        if len(routeToShift) > 0:
            # assign LT_CUSTOMERS into existing routes
            for ri in range(0, len(new_routes)):
                routeRi = new_routes[ri]
                # if totalRouteDistance(routeToShift) <= redumean <= totalRouteDistance(routeRi):
                #     route, routeToShift = initialSolution.assignLT_CUSTOMERS(routeRi, routeToShift, vehicle_capacity)
                #     new_routes[ri] = route
                # else:
                #     if totalRouteDistance(routeToShift) >= redumean >= totalRouteDistance(routeRi):
                #         route, routeToShift = initialSolution.assignLT_CUSTOMERS(routeRi, routeToShift, vehicle_capacity)
                #         new_routes[ri] = route
                if routeToShiftDistance >= redumean >= totalRouteDistance(pd.concat([depot, routeRi, depot])):
                    route, routeToShift = initialSolution.assignLT_CUSTOMERS(routeRi, routeToShift, vehicle_capacity)
                    new_routes[ri] = route
                else:
                    if routeToShiftDistance <= redumean <= totalRouteDistance(pd.concat([depot, routeRi, depot])):
                        route, routeToShift = initialSolution.assignLT_CUSTOMERS(routeRi, routeToShift, vehicle_capacity)
                        new_routes[ri] = route

        if len(routeToShift) > 0:
            new_routes.append(routeToShift)

        new_distances = 0
        for di in range(0, len(new_routes)):
            new_distances += totalRouteDistance(pd.concat([depot, new_routes[di], depot], ignore_index=False, axis=0))

            # assign remaining LT_CUSTOMERS into new routes the way MT_CUSTOMERS were assigned
            # if len(routeToShift) > 0:
            #     while len(routeToShift) > 0:
            #         route, routeToShift = initialSolution.assignMT_CUSTOMERS(routeToShift, vehicle_capacity)
            #         new_routes.append(route)

        if new_distances < best_distances or new_distances < distances:
            # print(f'nd - {new_distances}  bd - {distances}')
            return new_routes

        # print(sum(len(x) for x in new_routes))
        # print(len(new_routes))

    if new_distances > distances:
        return routes
    else:
        return new_routes

    # return new_routes


def upgradeRoutes2(routes, upgradeAttempts, vehicle_capacity, depot, best_distances):

    new_routes = copy.deepcopy(routes)
    toRemove = []

    for ri in range(0, len(routes)):
        for rci in routes[ri].index:
            toRemove.append([ri, rci])


    for ti in range(0, len(toRemove)):


        old_distances = 0
        for di in range(0, len(new_routes)):
            old_distances += totalRouteDistance(pd.concat([depot, new_routes[di], depot], ignore_index=False, axis=0))


        routeIndex = toRemove[ti][0]
        customerIndex = toRemove[ti][1]
        currentRoute = copy.deepcopy(new_routes[routeIndex])
        currentCustomer = currentRoute.loc[[customerIndex]]
        currentRoute.drop(customerIndex, axis=0, inplace=True)

        modified_routes = copy.deepcopy(new_routes)
        modified_routes[routeIndex] = currentRoute


        # print(customerIndex, currentCustomer)

        n = len(new_routes)
        for ri in range(0, n):
            if routeIndex != ri:
                routeToModify = copy.deepcopy(new_routes[ri])
                # old_distances = totalRouteDistance(pd.concat([depot, routeToModify, depot], ignore_index=False, axis=0))

                routeToModify, currentCustomer = initialSolution.assignLT_CUSTOMERS(routeToModify, currentCustomer,
                                                                                    vehicle_capacity)
                modified_routes[ri] = routeToModify

                new_distances = 0
                for di in range(0, len(new_routes)):
                    new_distances += totalRouteDistance(
                        pd.concat([depot, modified_routes[di], depot], ignore_index=False, axis=0))

                # new_distances = totalRouteDistance(pd.concat([depot, routeToModify, depot], ignore_index=False, axis=0))

                if len(currentCustomer) == 0 and new_distances < old_distances:
                    # print(f'{new_distances}, {old_distances}')
                    new_routes = modified_routes
                    break


    # print(new_routes)

    return new_routes

