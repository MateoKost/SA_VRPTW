EPOCH_START = 1
EPOCH = 100
ITER = 200
TZERO = 80
ALPHA = 0.965
MT_CLIENT_C1 = 5
LT_CLIENT_C1 = 2
PROPORTION_CNUMBER = 0.15
PROPABILITY_CNUMBER = 0.2
RADIUS_SCALAR = 2
UPGRADE_ATTEMPTS = 5
N_ROUTES_WEIGHT = 1000
DISTANCES_WEIGHT = 1


def decreaseTemperatureFunction(temperature): return ALPHA * temperature


def objectiveFunction(numberOfRoutes, distances):
    return N_ROUTES_WEIGHT * numberOfRoutes + DISTANCES_WEIGHT * distances
