"""
Configuration parameters for the water rocket simulation.
"""

# Physical constants
GRAVITY = 9.81  # m/s^2
AIR_DENSITY = 1.225  # kg/m^3
WATER_DENSITY = 1000.0  # kg/m^3
GAS_CONSTANT = 287.05  # J/(kg*K)
ATMOSPHERIC_PRESSURE = 101325.0  # Pa
TEMPERATURE = 293.15  # K (20°C)
LAUNCH_ANGLE = 10.0  # degrees (0 = vertical, positive angles towards positive x direction)

# Rocket parameters
BOTTLE_VOLUME = 2.5  # liters
BOTTLE_MASS = 0.05  # kg
WATER_VOLUME_FRACTION = 0.4  # fraction of bottle filled with water
NOZZLE_DIAMETER = 0.01  # m
NOZZLE_AREA = 3.14159 * (NOZZLE_DIAMETER/2)**2  # m^2
DRAG_COEFFICIENT = 0.3  # dimensionless
ROCKET_DIAMETER = 0.12  # m
ROCKET_CROSS_SECTION = 3.14159 * (ROCKET_DIAMETER/2)**2  # m^2
INITIAL_PRESSURE = 7 * 100000.0  # Pa (gauge pressure)
PAYLOAD_MASS = 0.4  # kg

# Simulation parameters
TIME_STEP = 0.001  # seconds
MAX_SIMULATION_TIME = 30.0  # seconds
