EPOCH = 100
ITER = 200
TZERO = 80

ALPHA = 0.965

VEHICLE_CAPACITY_C1 = 200

# experiment based
MT_CLIENT_C1 = 5
LT_CLIENT_C1 = 2

PROPORTION_CNUMBER = 0.1
PROPABILITY_CNUMBER = 0.2

def decreaseTemperatureFunction(temperature): return ALPHA * temperature
