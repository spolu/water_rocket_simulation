"""
Physics module for water rocket simulation.
Contains functions for calculating forces, accelerations, and state updates.
"""

import math
import config  # Import as module to ensure latest values are used

def calculate_mass(state):
    """
    Calculate the total mass of the rocket based on current state.
    
    Args:
        state: Current state dictionary containing water_mass
        
    Returns:
        Total mass in kg
    """
    return config.BOTTLE_MASS + state['water_mass'] + config.PAYLOAD_MASS


def calculate_water_mass(water_volume):
    """
    Calculate the mass of water based on its volume.
    
    Args:
        water_volume: Volume of water in m^3
        
    Returns:
        Mass of water in kg
    """
    return water_volume * config.WATER_DENSITY


def calculate_air_pressure(state):
    """
    Calculate the air pressure inside the bottle using ideal gas law.
    
    Args:
        state: Current state dictionary containing air_volume
        
    Returns:
        Air pressure in Pa
    """
    if state['water_mass'] <= 0:
        # All water expelled, air expands to fill the entire bottle
        new_pressure = state['air_pressure'] * (state['air_volume_initial'] / (config.BOTTLE_VOLUME / 1000))
        # Ensure pressure doesn't fall below atmospheric pressure
        return max(new_pressure, config.ATMOSPHERIC_PRESSURE)
    
    # Use the ideal gas law with adiabatic expansion: P1 * V1^gamma = P2 * V2^gamma
    # gamma = 1.4 for air (adiabatic index)
    gamma = 1.4
    new_pressure = state['air_pressure_initial'] * (state['air_volume_initial'] / state['air_volume']) ** gamma
    # Ensure pressure doesn't fall below atmospheric pressure
    return max(new_pressure, config.ATMOSPHERIC_PRESSURE)


def calculate_water_acceleration(state):
    """
    Calculate the acceleration of water out of the nozzle.
    
    Args:
        state: Current state dictionary
        
    Returns:
        Acceleration of water in m/s^2
    """
    if state['water_mass'] <= 0:
        return 0
    
    # Pressure difference driving the water out
    pressure_diff = state['air_pressure'] - config.ATMOSPHERIC_PRESSURE
    
    # If pressure difference is negative or zero, no water comes out
    if pressure_diff <= 0:
        return 0
    
    # Calculate water velocity using Bernoulli's equation
    # v = sqrt(2 * pressure_diff / water_density)
    water_velocity = math.sqrt(2 * pressure_diff / config.WATER_DENSITY)
    
    # Calculate water mass flow rate
    # dm/dt = density * area * velocity
    water_mass_flow_rate = config.WATER_DENSITY * config.NOZZLE_AREA * water_velocity
    
    return water_mass_flow_rate


def calculate_thrust(state):
    """
    Calculate the thrust produced by water/air expulsion.
    
    Args:
        state: Current state dictionary
        
    Returns:
        Thrust force in N
    """
    if state['water_mass'] <= 0:
        # Air-only thrust phase
        if state['air_pressure'] <= config.ATMOSPHERIC_PRESSURE:
            return 0
        
        # Calculate air density inside the bottle
        air_density = state['air_pressure'] / (config.GAS_CONSTANT * config.TEMPERATURE)
        
        # Calculate air velocity using Bernoulli's equation
        # Ensure pressure difference is positive to avoid math domain error
        pressure_diff = max(0, state['air_pressure'] - config.ATMOSPHERIC_PRESSURE)
        air_velocity = math.sqrt(2 * pressure_diff / air_density)
        
        # Calculate air mass flow rate
        air_mass_flow_rate = air_density * config.NOZZLE_AREA * air_velocity
        
        # Thrust = mass flow rate * velocity
        return air_mass_flow_rate * air_velocity
    else:
        # Water thrust phase
        # Ensure pressure difference is positive to avoid math domain error
        pressure_diff = max(0, state['air_pressure'] - config.ATMOSPHERIC_PRESSURE)
        water_velocity = math.sqrt(2 * pressure_diff / config.WATER_DENSITY)
        water_mass_flow_rate = config.WATER_DENSITY * config.NOZZLE_AREA * water_velocity
        
        # Thrust = mass flow rate * velocity
        return water_mass_flow_rate * water_velocity


def calculate_drag(state):
    """
    Calculate the aerodynamic drag force.
    
    Args:
        state: Current state dictionary containing velocity
        
    Returns:
        Drag force in N (vertical component only)
    """
    # Drag equation: F_drag = 0.5 * rho * v^2 * Cd * A
    velocity = state['velocity']
    drag_force = 0.5 * config.AIR_DENSITY * velocity**2 * config.DRAG_COEFFICIENT * config.ROCKET_CROSS_SECTION
    
    # Drag acts in the opposite direction of velocity
    if velocity > 0:
        return -drag_force
    else:
        return drag_force


def calculate_thrust_components(thrust, angle_rad):
    """
    Calculate the vertical and horizontal components of thrust based on launch angle.
    
    Args:
        thrust: Total thrust force in N
        angle_rad: Launch angle in radians
        
    Returns:
        Tuple of (vertical_thrust, horizontal_thrust) in N
    """
    # Vertical component (reduced by cosine of angle)
    vertical_thrust = thrust * math.cos(angle_rad)
    
    # Horizontal component (determined by sine of angle)
    horizontal_thrust = thrust * math.sin(angle_rad)
    
    return vertical_thrust, horizontal_thrust


def calculate_gravity_force(state):
    """
    Calculate the gravitational force.
    
    Args:
        state: Current state dictionary
        
    Returns:
        Gravitational force in N
    """
    return -calculate_mass(state) * config.GRAVITY


def calculate_net_force(state):
    """
    Calculate the net force acting on the rocket.
    
    Args:
        state: Current state dictionary
        
    Returns:
        Tuple of (vertical_force, horizontal_force) in N
    """
    # Calculate total thrust
    thrust = calculate_thrust(state)
    
    # Convert launch angle from degrees to radians
    angle_rad = math.radians(config.LAUNCH_ANGLE)
    
    # Calculate thrust components
    vertical_thrust, horizontal_thrust = calculate_thrust_components(thrust, angle_rad)
    
    # Calculate other vertical forces
    drag = calculate_drag(state)
    gravity = calculate_gravity_force(state)
    
    # Net vertical and horizontal forces
    vertical_force = vertical_thrust + drag + gravity
    horizontal_force = horizontal_thrust
    
    return vertical_force, horizontal_force


def calculate_acceleration(state):
    """
    Calculate the acceleration of the rocket.
    
    Args:
        state: Current state dictionary
        
    Returns:
        Tuple of (vertical_acceleration, horizontal_acceleration) in m/s^2
    """
    vertical_force, horizontal_force = calculate_net_force(state)
    mass = calculate_mass(state)
    
    # F = ma, so a = F/m
    vertical_acceleration = vertical_force / mass
    horizontal_acceleration = horizontal_force / mass
    
    return vertical_acceleration, horizontal_acceleration


def update_state(state, dt):
    """
    Update the state of the rocket for the next time step.
    
    Args:
        state: Current state dictionary
        dt: Time step in seconds
        
    Returns:
        Updated state dictionary
    """
    # Make a copy of the current state
    new_state = state.copy()
    
    # Update water mass if water is still being expelled
    if state['water_mass'] > 0:
        water_expelled = calculate_water_acceleration(state) * dt
        new_state['water_mass'] = max(0, state['water_mass'] - water_expelled)
        
        # Update air volume as water is expelled
        water_volume_change = water_expelled / config.WATER_DENSITY
        new_state['air_volume'] = state['air_volume'] + water_volume_change
    
    # Update air pressure
    new_state['air_pressure'] = calculate_air_pressure(new_state)
    
    # Calculate vertical and horizontal accelerations
    vertical_acceleration, horizontal_acceleration = calculate_acceleration(new_state)
    
    # Update vertical velocity and position
    new_state['acceleration'] = vertical_acceleration  # Store vertical acceleration for backward compatibility
    new_state['velocity'] = state['velocity'] + vertical_acceleration * dt
    new_state['position'] = state['position'] + new_state['velocity'] * dt
    
    # Update horizontal velocity and position
    new_state['x_acceleration'] = horizontal_acceleration
    new_state['x_velocity'] = state.get('x_velocity', 0) + horizontal_acceleration * dt
    new_state['x_position'] = state.get('x_position', 0) + new_state['x_velocity'] * dt
    
    # Update time
    new_state['time'] = state['time'] + dt
    
    return new_state
