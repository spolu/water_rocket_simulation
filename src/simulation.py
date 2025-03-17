"""
Simulation module for water rocket physics.
Handles the time-stepping and state tracking of the rocket simulation.
"""

# No external dependencies needed
import config  # Import as module to ensure latest values are used
from physics import update_state


def initialize_state():
    """
    Initialize the state dictionary with starting values.
    
    Returns:
        Dictionary containing initial state values
    """
    # Calculate initial water volume in m^3 (per bottles)
    water_volume = (config.BOTTLE_VOLUME / 1000) * config.WATER_VOLUME_FRACTION 
    
    # Calculate initial air volume in m^3 (per bottles)
    air_volume = (config.BOTTLE_VOLUME / 1000) * (1 - config.WATER_VOLUME_FRACTION)

    # Calculate initial water mass (for all bottles)
    water_mass = water_volume * config.WATER_DENSITY
    
    # Initial state dictionary
    state = {
        'time': 0.0,
        'position': 0.0,  # Initial height (m)
        'x_position': 0.0,  # Initial horizontal position (m)
        'velocity': 0.0,  # Initial vertical velocity (m/s)
        'x_velocity': 0.0,  # Initial horizontal velocity (m/s)
        'acceleration': 0.0,  # Initial vertical acceleration (m/s^2)
        'water_mass': water_mass,  # Mass of water (kg)
        'air_volume': air_volume,  # Volume of air (m^3)
        'air_volume_initial': air_volume,  # Initial volume of air (m^3)
        'air_pressure': config.ATMOSPHERIC_PRESSURE + config.INITIAL_PRESSURE,  # Total pressure (Pa)
        'air_pressure_initial': config.ATMOSPHERIC_PRESSURE + config.INITIAL_PRESSURE,  # Initial pressure (Pa)
    }
    
    return state


def run_simulation():
    """
    Run the complete water rocket simulation.
    
    Returns:
        List of state dictionaries for each time step
    """
    # Initialize state
    state = initialize_state()
    
    # List to store states at each time step
    states = [state.copy()]
    
    # Run simulation until rocket hits the ground or max time is reached
    while (state['position'] >= 0 or state['velocity'] > 0) and state['time'] < config.MAX_SIMULATION_TIME:
        # Update state for next time step
        state = update_state(state, config.TIME_STEP)
        
        # Store state
        states.append(state.copy())
        
        # Check if rocket has hit the ground
        if state['position'] < 0 and state['velocity'] < 0:
            # Adjust final position to be exactly at ground level
            state['position'] = 0
            states[-1] = state.copy()
            break
    
    return states


def extract_trajectory_data(states):
    """
    Extract trajectory data from states for plotting and analysis.
    
    Args:
        states: List of state dictionaries
        
    Returns:
        Dictionary of trajectory data arrays
    """
    # Extract data
    times = [state['time'] for state in states]
    positions = [state['position'] for state in states]
    x_positions = [state['x_position'] for state in states]
    velocities = [state['velocity'] for state in states]
    x_velocities = [state.get('x_velocity', 0) for state in states]  # Use get() to handle missing keys
    accelerations = [state['acceleration'] for state in states]
    water_masses = [state['water_mass'] for state in states]
    air_pressures = [state['air_pressure'] for state in states]
    
    # Find water expulsion time
    water_expulsion_time = times[0]
    for i, mass in enumerate(water_masses):
        if mass <= 0:
            water_expulsion_time = times[i]
            break
    
    # Find apogee (maximum height)
    apogee_height = max(positions)
    apogee_time = times[positions.index(apogee_height)]
    
    # Find flight time
    flight_time = times[-1]
    
    # Find maximum velocity
    max_velocity = max(velocities)
    max_velocity_time = times[velocities.index(max_velocity)]
    
    # Find maximum acceleration
    max_acceleration = max(accelerations)
    max_acceleration_time = times[accelerations.index(max_acceleration)]
    
    # Compile results
    trajectory_data = {
        'times': times,
        'positions': positions,
        'x_positions': x_positions,
        'velocities': velocities,
        'x_velocities': x_velocities,
        'accelerations': accelerations,
        'water_masses': water_masses,
        'air_pressures': air_pressures,
        'water_expulsion_time': water_expulsion_time,
        'apogee_height': apogee_height,
        'apogee_time': apogee_time,
        'flight_time': flight_time,
        'max_velocity': max_velocity,
        'max_velocity_time': max_velocity_time,
        'max_acceleration': max_acceleration,
        'max_acceleration_time': max_acceleration_time
    }
    
    return trajectory_data
