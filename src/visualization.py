"""
Visualization module for water rocket simulation.
Provides functions for plotting trajectory and performance data.
"""

import matplotlib.pyplot as plt
import numpy as np
from config import *


def plot_height_vs_time(trajectory_data):
    """
    Plot the height vs time trajectory of the rocket.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_data['times'], trajectory_data['positions'])
    
    # Mark key points
    plt.axvline(x=trajectory_data['water_expulsion_time'], color='blue', linestyle='--', 
                label=f'Water Expulsion ({trajectory_data["water_expulsion_time"]:.2f} s)')
    plt.scatter(trajectory_data['apogee_time'], trajectory_data['apogee_height'], color='red', 
                label=f'Apogee: {trajectory_data["apogee_height"]:.2f} m at {trajectory_data["apogee_time"]:.2f} s')
    
    plt.title('Water Rocket Height vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_trajectory_2d(trajectory_data):
    """
    Plot the 2D trajectory of the rocket (x vs y).
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 10))  # Square figure for better 1:1 ratio
    plt.plot(trajectory_data['x_positions'], trajectory_data['positions'])
    
    # Mark key points
    water_expulsion_index = next((i for i, t in enumerate(trajectory_data['times']) 
                               if t >= trajectory_data['water_expulsion_time']), 0)
    plt.scatter(trajectory_data['x_positions'][water_expulsion_index], 
                trajectory_data['positions'][water_expulsion_index], 
                color='blue', 
                label=f'Water Expulsion')
    
    # Find apogee index
    apogee_index = trajectory_data['positions'].index(trajectory_data['apogee_height'])
    plt.scatter(trajectory_data['x_positions'][apogee_index], 
                trajectory_data['positions'][apogee_index], 
                color='red', 
                label=f'Apogee: {trajectory_data["apogee_height"]:.2f} m')
    
    plt.title('Water Rocket 2D Trajectory')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Height (m)')
    
    # Set aspect ratio to be equal (1:1)
    plt.axis('equal')
    
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_velocity(trajectory_data):
    """
    Plot the velocity vs time of the rocket.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_data['times'], trajectory_data['velocities'])
    
    # Mark key points
    plt.axvline(x=trajectory_data['water_expulsion_time'], color='blue', linestyle='--', 
                label=f'Water Expulsion ({trajectory_data["water_expulsion_time"]:.2f} s)')
    plt.scatter(trajectory_data['max_velocity_time'], trajectory_data['max_velocity'], color='red', 
                label=f'Max Velocity: {trajectory_data["max_velocity"]:.2f} m/s at {trajectory_data["max_velocity_time"]:.2f} s')
    
    plt.title('Water Rocket Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_acceleration(trajectory_data):
    """
    Plot the acceleration vs time of the rocket.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_data['times'], trajectory_data['accelerations'])
    
    # Mark key points
    plt.axvline(x=trajectory_data['water_expulsion_time'], color='blue', linestyle='--', 
                label=f'Water Expulsion ({trajectory_data["water_expulsion_time"]:.2f} s)')
    plt.scatter(trajectory_data['max_acceleration_time'], trajectory_data['max_acceleration'], color='red', 
                label=f'Max Acceleration: {trajectory_data["max_acceleration"]:.2f} m/s² at {trajectory_data["max_acceleration_time"]:.2f} s')
    
    plt.title('Water Rocket Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_pressure(trajectory_data):
    """
    Plot the air pressure vs time inside the rocket.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_data['times'], np.array(trajectory_data['air_pressures']) / 1000)  # Convert to kPa
    
    # Mark water expulsion
    plt.axvline(x=trajectory_data['water_expulsion_time'], color='blue', linestyle='--', 
                label=f'Water Expulsion ({trajectory_data["water_expulsion_time"]:.2f} s)')
    
    plt.title('Air Pressure Inside Rocket')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (kPa)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_water_mass(trajectory_data):
    """
    Plot the water mass vs time in the rocket.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    plt.figure(figsize=(10, 6))
    plt.plot(trajectory_data['times'], trajectory_data['water_masses'])
    
    # Mark water expulsion
    plt.axvline(x=trajectory_data['water_expulsion_time'], color='blue', linestyle='--', 
                label=f'Water Expulsion ({trajectory_data["water_expulsion_time"]:.2f} s)')
    
    plt.title('Water Mass in Rocket')
    plt.xlabel('Time (s)')
    plt.ylabel('Water Mass (kg)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    return plt.gcf()


def plot_all(trajectory_data, save_path=None):
    """
    Create and save all plots for the rocket simulation.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
        save_path: Optional path to save the plots
    """
    # Create individual plots
    plot_height_vs_time(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/height_vs_time.png", dpi=300)
        
    plot_trajectory_2d(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/trajectory_2d.png", dpi=300)
    
    plot_velocity(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/velocity.png", dpi=300)
    
    plot_acceleration(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/acceleration.png", dpi=300)
    
    plot_pressure(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/pressure.png", dpi=300)
    
    plot_water_mass(trajectory_data)
    if save_path:
        plt.savefig(f"{save_path}/water_mass.png", dpi=300)
    
    # Create summary plot with key metrics
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    plt.text(0.5, 0.9, 'Water Rocket Simulation Summary', horizontalalignment='center', fontsize=16)
    
    summary_text = f"""
    Maximum Height: {trajectory_data['apogee_height']:.2f} m at {trajectory_data['apogee_time']:.2f} s
    Maximum Velocity: {trajectory_data['max_velocity']:.2f} m/s at {trajectory_data['max_velocity_time']:.2f} s
    Maximum Acceleration: {trajectory_data['max_acceleration']:.2f} m/s² at {trajectory_data['max_acceleration_time']:.2f} s
    Water Expulsion Time: {trajectory_data['water_expulsion_time']:.2f} s
    Total Flight Time: {trajectory_data['flight_time']:.2f} s
    Horizontal Distance: {trajectory_data['x_positions'][-1]:.2f} m
    
    Rocket Parameters:
    - Bottle Volume: {BOTTLE_VOLUME} L
    - Water Fill: {WATER_VOLUME_FRACTION * 100:.1f}%
    - Initial Pressure: {INITIAL_PRESSURE / 1000:.1f} kPa (gauge)
    - Nozzle Diameter: {NOZZLE_DIAMETER * 1000:.1f} mm
    - Rocket Mass (empty): {BOTTLE_MASS + PAYLOAD_MASS:.3f} kg
    - Wind Speed: {WIND_SPEED:.1f} m/s
    """
    
    plt.text(0.5, 0.5, summary_text, horizontalalignment='center', verticalalignment='center', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(f"{save_path}/summary.png", dpi=300)
    
    return plt.gcf()


def display_summary(trajectory_data):
    """
    Display a summary of the simulation results.
    
    Args:
        trajectory_data: Dictionary containing trajectory data arrays
    """
    print("\n=== WATER ROCKET SIMULATION SUMMARY ===")
    print(f"Maximum Height: {trajectory_data['apogee_height']:.2f} m at {trajectory_data['apogee_time']:.2f} s")
    print(f"Maximum Velocity: {trajectory_data['max_velocity']:.2f} m/s at {trajectory_data['max_velocity_time']:.2f} s")
    print(f"Maximum Acceleration: {trajectory_data['max_acceleration']:.2f} m/s² at {trajectory_data['max_acceleration_time']:.2f} s")
    print(f"Water Expulsion Time: {trajectory_data['water_expulsion_time']:.2f} s")
    print(f"Total Flight Time: {trajectory_data['flight_time']:.2f} s")
    print("\nRocket Parameters:")
    print(f"- Bottle Volume: {BOTTLE_VOLUME} L")
    print(f"- Water Fill: {WATER_VOLUME_FRACTION * 100:.1f}%")
    print(f"- Initial Pressure: {INITIAL_PRESSURE / 1000:.1f} kPa (gauge)")
    print(f"- Nozzle Diameter: {NOZZLE_DIAMETER * 1000:.1f} mm")
    print(f"- Rocket Mass (empty): {BOTTLE_MASS + PAYLOAD_MASS:.3f} kg")
    print("========================================")
