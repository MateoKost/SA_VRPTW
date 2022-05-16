EPOCH = 100
ITER = 200
TZERO = 80
# TZERO = 19.239001156514032
ALPHA = 0.965
# experiment based
MT_CLIENT_C1 = 5
LT_CLIENT_C1 = 2
PROPORTION_CNUMBER = 0.2
PROPABILITY_CNUMBER = 0.25
RADIUS_SCALAR = 2

UPGRADE_ATTEMPTS = 4

N_ROUTES_WEIGHT = 0
DISTANCES_WEIGHT = 1


def decreaseTemperatureFunction(temperature): return ALPHA * temperature


def objectiveFunction(numberOfRoutes, distances):
    return N_ROUTES_WEIGHT * numberOfRoutes + DISTANCES_WEIGHT * distances
