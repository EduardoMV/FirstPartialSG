import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from EUMV_FMS import run_all_runs

def generate_visualizations(all_results):
    # Set the style for plots
    sns.set_theme(style="whitegrid")
    
    # Extract key metrics from all_results
    productions = [result['production'] for result in all_results]
    rejections = [result['rejected'] for result in all_results]
    defect_rates = [rej / (prod + rej) if (prod + rej) > 0 else 0 for prod, rej in zip(productions, rejections)]
    supplier_occs = [result['supplier_occupancy'] for result in all_results]

    # Plot 1: Production and Defect Rates
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.boxplot(x=productions)
    plt.title('Production per Run')
    plt.xlabel('Total Production')

    plt.subplot(1, 2, 2)
    sns.boxplot(x=defect_rates)
    plt.title('Defect Rate per Run')
    plt.xlabel('Defect Rate')
    plt.tight_layout()
    plt.savefig('production_defect_rates.png')  # Save as PNG
    plt.close()

    # Plot 2: Station Occupancy Rates
    occupancy_data = []
    for station in range(6):
        occupancies = [result['stations'][station]['occupancy'] for result in all_results]  # Use integer key
        occupancy_data.append(occupancies)
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=occupancy_data)
    plt.xticks(range(6), [f'Station {i}' for i in range(6)])
    plt.title('Station Occupancy Rates')
    plt.ylabel('Occupancy Rate')
    plt.savefig('station_occupancy_rates.png')  # Save as PNG
    plt.close()

    # Plot 3: Station Downtime
    downtime_data = []
    for station in range(6):
        downtimes = [result['stations'][station]['downtime'] for result in all_results]  # Use integer key
        downtime_data.append(downtimes)
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=downtime_data)
    plt.xticks(range(6), [f'Station {i}' for i in range(6)])
    plt.title('Station Downtime')
    plt.ylabel('Downtime (Units)')
    plt.savefig('station_downtime.png')  # Save as PNG
    plt.close()

    # Plot 4: Supplier Utilization
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=supplier_occs)
    plt.title('Supplier Utilization Rate')
    plt.xlabel('Utilization Rate')
    plt.savefig('supplier_utilization.png')  # Save as PNG
    plt.close()

    # Plot 5: Average Fixing Time per Station
    fixing_data = []
    for station in range(6):
        fixes = [result['stations'][station]['avg_fixing_time'] for result in all_results]  # Use integer key
        fixing_data.append(fixes)
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=fixing_data)
    plt.xticks(range(6), [f'Station {i}' for i in range(6)])
    plt.title('Average Fixing Time per Station')
    plt.ylabel('Fixing Time (Units)')
    plt.savefig('average_fixing_time.png')  # Save as PNG
    plt.close()

    # Plot 6: Bottleneck Delays
    bottleneck_data = []
    for station in range(6):
        delays = [result['stations'][station]['avg_bottleneck_delay'] for result in all_results]  # Use integer key
        bottleneck_data.append(delays)
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=bottleneck_data)
    plt.xticks(range(6), [f'Station {i}' for i in range(6)])
    plt.title('Average Bottleneck Delay per Station')
    plt.ylabel('Delay (Units)')
    plt.savefig('bottleneck_delays.png')  # Save as PNG
    plt.close()

if __name__ == "__main__":
    # Run simulations and generate visualizations
    simulation_results = run_all_runs(num_runs=100, simulation_time=5000)
    generate_visualizations(simulation_results)