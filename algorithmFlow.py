from Preliminaries import *
import utils
import math


def run(fdata):
    # utils.measureTime(123)

    # print(fdata['CUST NO.'])
    tour = fdata["CUST NO."].values
    # print(tour)
    distance = totaldistancetour(fdata, tour)
    print(f'distance - {distance}')

    # min distance
    #



def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def totaldistancetour(customers, tour):
    d=0
    for i in range(1,len(tour)):
        customerPrevious = customers[customers['CUST NO.'] == tour[i - 1]]
        x1 = customerPrevious['XCOORD.'].values[0]
        y1 = customerPrevious['YCOORD.'].values[0]

        customerAtTourMoment = customers[customers['CUST NO.'] == tour[i]]
        x2 = customerAtTourMoment['XCOORD.'].values[0]
        y2 = customerAtTourMoment['YCOORD.'].values[0]

        d = d + distance(x1, y1, x2, y2)
    return d