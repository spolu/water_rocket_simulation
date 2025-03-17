"""
Main script for water rocket simulation.
Runs the simulation and generates visualizations.
"""

import os
import argparse
import csv
from simulation import run_simulation, extract_trajectory_data
import config


def create_output_directory():
    """Create output directory for saving results if it doesn't exist."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def save_data_to_csv(trajectory_data, output_dir):
    """Save simulation data to CSV files."""
    # Save trajectory data
    with open(f"{output_dir}/trajectory.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'Height (m)', 'Velocity (m/s)', 'Acceleration (m/s²)', 
                       'Water Mass (kg)', 'Air Pressure (Pa)'])
        for i in range(len(trajectory_data['times'])):
            writer.writerow([
                trajectory_data['times'][i],
                trajectory_data['positions'][i],
                trajectory_data['velocities'][i],
                trajectory_data['accelerations'][i],
                trajectory_data['water_masses'][i],
                trajectory_data['air_pressures'][i]
            ])
    
    # Save summary data
    with open(f"{output_dir}/summary.txt", 'w') as f:
        f.write("=== WATER ROCKET SIMULATION SUMMARY ===\n")
        f.write(f"Maximum Height: {trajectory_data['apogee_height']:.2f} m at {trajectory_data['apogee_time']:.2f} s\n")
        f.write(f"Maximum Velocity: {trajectory_data['max_velocity']:.2f} m/s at {trajectory_data['max_velocity_time']:.2f} s\n")
        f.write(f"Maximum Acceleration: {trajectory_data['max_acceleration']:.2f} m/s² at {trajectory_data['max_acceleration_time']:.2f} s\n")
        f.write(f"Water Expulsion Time: {trajectory_data['water_expulsion_time']:.2f} s\n")
        f.write(f"Total Flight Time: {trajectory_data['flight_time']:.2f} s\n")
        f.write("\nRocket Parameters:\n")
        f.write(f"- Bottle Volume: {config.BOTTLE_VOLUME} L\n")
        f.write(f"- Water Fill: {config.WATER_VOLUME_FRACTION * 100:.1f}%\n")
        f.write(f"- Initial Pressure: {config.INITIAL_PRESSURE / 1000:.1f} kPa (gauge)\n")
        f.write(f"- Nozzle Diameter: {config.NOZZLE_DIAMETER * 1000:.1f} mm\n")
        f.write(f"- Rocket Mass (empty): {config.BOTTLE_MASS + config.PAYLOAD_MASS:.3f} kg\n")
        f.write("========================================\n")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Water Rocket Simulation')
    parser.add_argument('--bottle-volume', type=float, default=config.BOTTLE_VOLUME,
                        help='Bottle volume in liters')
    parser.add_argument('--water-fraction', type=float, default=config.WATER_VOLUME_FRACTION,
                        help='Fraction of bottle filled with water (0-1)')
    parser.add_argument('--pressure', type=float, default=config.INITIAL_PRESSURE / 1000,
                        help='Initial gauge pressure in kPa')
    parser.add_argument('--nozzle-diameter', type=float, default=config.NOZZLE_DIAMETER * 1000,
                        help='Nozzle diameter in mm')
    parser.add_argument('--launch-angle', type=float, default=config.LAUNCH_ANGLE,
                        help='Launch angle in degrees (0 = vertical, positive angles towards positive x direction)')
    parser.add_argument('--save-data', action='store_true',
                        help='Save data to CSV files in output directory')
    parser.add_argument('--sweep', action='store_true',
                        help='Run water fraction parameter sweep')
    parser.add_argument('--n-values', type=int, default=10,
                        help='Number of values to use in parameter sweep')
    return parser.parse_args()


def update_config(args):
    """Update configuration based on command line arguments."""
    config.BOTTLE_VOLUME = args.bottle_volume
    config.WATER_VOLUME_FRACTION = args.water_fraction
    config.INITIAL_PRESSURE = args.pressure * 1000  # Convert kPa to Pa
    config.NOZZLE_DIAMETER = args.nozzle_diameter / 1000  # Convert mm to m
    config.NOZZLE_AREA = 3.14159 * (config.NOZZLE_DIAMETER/2)**2
    config.LAUNCH_ANGLE = args.launch_angle


def display_summary(trajectory_data):
    """Display a summary of the simulation results."""
    print("\n=== WATER ROCKET SIMULATION SUMMARY ===")
    print(f"Maximum Height: {trajectory_data['apogee_height']:.2f} m at {trajectory_data['apogee_time']:.2f} s")
    print(f"Maximum Velocity: {trajectory_data['max_velocity']:.2f} m/s at {trajectory_data['max_velocity_time']:.2f} s")
    print(f"Maximum Acceleration: {trajectory_data['max_acceleration']:.2f} m/s² at {trajectory_data['max_acceleration_time']:.2f} s")
    print(f"Water Expulsion Time: {trajectory_data['water_expulsion_time']:.2f} s")
    print(f"Total Flight Time: {trajectory_data['flight_time']:.2f} s")
    print("\nRocket Parameters:")
    print(f"- Bottle Volume: {config.BOTTLE_VOLUME} L")
    print(f"- Water Fill: {config.WATER_VOLUME_FRACTION * 100:.1f}%")
    print(f"- Initial Pressure: {config.INITIAL_PRESSURE / 1000:.1f} kPa (gauge)")
    print(f"- Nozzle Diameter: {config.NOZZLE_DIAMETER * 1000:.1f} mm")
    print(f"- Rocket Mass (empty): {config.BOTTLE_MASS + config.PAYLOAD_MASS:.3f} kg")
    print("========================================")


def main():
    """Main function to run the simulation."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Update configuration if needed
    update_config(args)
    
    # Create output directory
    output_dir = create_output_directory() if args.save_data else None
    
    # Run parameter sweep if requested
    if args.sweep:
        water_fraction_sweep(launch_angle=args.launch_angle, n_values=args.n_values)
        return
    
    # Run the simulation
    print("Running water rocket simulation...")
    states = run_simulation()
    
    # Extract trajectory data
    trajectory_data = extract_trajectory_data(states)
    
    # Display summary
    display_summary(trajectory_data)
    
    # Save data if requested
    if args.save_data:
        print(f"Saving data to {output_dir}...")
        save_data_to_csv(trajectory_data, output_dir)
    
    print("Simulation complete!")


def water_fraction_sweep(launch_angle=15.0, n_values=10):
    """
    Run a parameter sweep on water volume fraction and plot N trajectories.
    
    Args:
        launch_angle: Launch angle in degrees
        n_values: Number of water fraction values to sweep
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    
    # Save original parameters
    original_water_fraction = config.WATER_VOLUME_FRACTION
    original_launch_angle = config.LAUNCH_ANGLE
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Set launch angle
    config.LAUNCH_ANGLE = launch_angle
    
    # Generate N water fraction values between 0.1 and 0.9
    water_fractions = np.linspace(0.1, 0.9, n_values)
    
    # Results storage
    all_trajectory_data = []
    max_heights = []
    max_distances = []
    
    print(f"Running water fraction sweep with {n_values} values and launch angle of {launch_angle} degrees...")
    
    # Get a colormap for the trajectories
    import matplotlib as mpl
    cmap = mpl.colormaps['viridis']
    
    # Sweep through water fractions
    for i, water_fraction in enumerate(water_fractions):
        # Update configuration
        config.WATER_VOLUME_FRACTION = water_fraction
        
        # Run simulation
        states = run_simulation()
        trajectory_data = extract_trajectory_data(states)
        
        # Store results
        all_trajectory_data.append(trajectory_data)
        max_heights.append(trajectory_data['apogee_height'])
        max_distances.append(trajectory_data['x_positions'][-1])
        
        print(f"Water: {water_fraction*100:.1f}%, "
              f"Max Height: {trajectory_data['apogee_height']:.2f} m, "
              f"Horizontal Distance: {trajectory_data['x_positions'][-1]:.2f} m")
    
    # Save parameter sweep results to CSV
    with open(f"{output_dir}/water_fraction_sweep.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Water Fill %', 'Max Height (m)', 'Horizontal Distance (m)'])
        
        for i, water_fraction in enumerate(water_fractions):
            writer.writerow([f"{water_fraction*100:.1f}%", f"{max_heights[i]:.2f}", f"{max_distances[i]:.2f}"])
    
    # Plot all trajectories in 2D
    plt.figure(figsize=(10, 10))  # Square figure for better 1:1 ratio
    
    for i, trajectory_data in enumerate(all_trajectory_data):
        color = cmap(i / n_values)
        plt.plot(trajectory_data['x_positions'], trajectory_data['positions'], 
                 color=color, 
                 label=f"Water: {water_fractions[i]*100:.1f}%")
    
    plt.title(f'Water Rocket 2D Trajectories (Launch Angle: {launch_angle}°)')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Height (m)')
    
    # Set aspect ratio to be equal (1:1)
    plt.axis('equal')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f"{output_dir}/water_fraction_sweep_trajectories.png", dpi=300, bbox_inches='tight')
    
    # Plot water fraction vs max height
    plt.figure(figsize=(10, 6))
    plt.plot(water_fractions, max_heights, 'o-')
    plt.title('Effect of Water Fill on Maximum Height')
    plt.xlabel('Water Volume Fraction')
    plt.ylabel('Maximum Height (m)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/water_fraction_vs_height.png", dpi=300)
    
    # Plot water fraction vs horizontal distance
    plt.figure(figsize=(10, 6))
    plt.plot(water_fractions, max_distances, 'o-')
    plt.title('Effect of Water Fill on Horizontal Distance')
    plt.xlabel('Water Volume Fraction')
    plt.ylabel('Horizontal Distance (m)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/water_fraction_vs_distance.png", dpi=300)
    
    # Print parameter sweep results
    print("\n=== WATER FRACTION SWEEP RESULTS ===")
    print("Effect of Water Fill on Maximum Height and Horizontal Distance")
    print("-" * 70)
    print("Water Fill %\tMax Height (m)\tHorizontal Distance (m)")
    
    for i, water_fraction in enumerate(water_fractions):
        print(f"{water_fraction*100:.1f}%\t\t{max_heights[i]:.2f}\t\t{max_distances[i]:.2f}")
    
    # Restore original parameters
    config.WATER_VOLUME_FRACTION = original_water_fraction
    config.LAUNCH_ANGLE = original_launch_angle
    
    return all_trajectory_data


if __name__ == "__main__":
    main()
