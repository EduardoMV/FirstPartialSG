import time
import simpy
import numpy as np
from dataclasses import dataclass
from typing import List, Dict

np.random.seed(int(time.time()))

@dataclass
class StationMetrics:
    processed_items: int = 0
    busy_time: float = 0
    downtime: float = 0
    fixing_times: List[float] = None
    waiting_times: List[float] = None
    bottleneck_delays: List[float] = None
    
    def __post_init__(self):
        self.fixing_times = []
        self.waiting_times = []
        self.bottleneck_delays = []

class ManufacturingFacility:
    def __init__(self, env):
        self.env = env
        self.stations = [simpy.Resource(env, capacity=1) for _ in range(6)]
        self.bins = [25, 25, 25, 25, 25, 25]  # Optimized bin sizes
        self.suppliers = simpy.Resource(env, capacity=3)
        
        # Metrics
        self.metrics = {i: StationMetrics() for i in range(6)}
        self.total_production = 0
        self.rejected_products = 0
        self.supplier_busy_time = 0
        self.last_product_time = 0
        self.failure_probs = [0.02, 0.01, 0.05, 0.15, 0.07, 0.06]
        
    def resupply_bin(self, station_id):
        start_time = self.env.now
        with self.suppliers.request() as req:
            yield req
            delay = abs(np.random.normal(2, 0.5))  # More efficient resupply
            yield self.env.timeout(delay)
            self.bins[station_id] = 25 # Restore to original capacity
            self.supplier_busy_time += self.env.now - start_time

    def process_station(self, product_id, station_id, start_queue_time):
        # Record waiting time
        self.metrics[station_id].waiting_times.append(self.env.now - start_queue_time)
        
        # Process time
        process_time = abs(np.random.normal(4, 1))
        yield self.env.timeout(process_time)
        
        # Update metrics
        self.metrics[station_id].processed_items += 1
        self.metrics[station_id].busy_time += process_time
    
        if self.metrics[station_id].processed_items % 5 == 0:
            # Regular maintenance for other stations
            if np.random.random() < self.failure_probs[station_id]:
                fixing_time = np.random.exponential(3)
                yield self.env.timeout(fixing_time)
                self.metrics[station_id].downtime += fixing_time
                self.metrics[station_id].fixing_times.append(fixing_time)
                
        # Record bottleneck delay
        if self.last_product_time > 0:
            delay = self.env.now - self.last_product_time - process_time
            if delay > 0:
                self.metrics[station_id].bottleneck_delays.append(delay)
        self.last_product_time = self.env.now

    def process_product(self, product_id):
        # Process stations 0-3 sequentially
        for i in range(4):
            if self.bins[i] <= 0:
                yield self.env.process(self.resupply_bin(i))
            self.bins[i] -= 1
            
            start_queue = self.env.now
            with self.stations[i].request() as req:
                yield req
                yield self.env.process(self.process_station(product_id, i, start_queue))
        
        # Handle parallel stations 4 and 5
        # First parallel station
        start_queue = self.env.now
        if len(self.stations[4].queue) <= len(self.stations[5].queue):
            parallel_first = 4
        else:
            parallel_first = 5
            
        if self.bins[parallel_first] <= 0:
            yield self.env.process(self.resupply_bin(parallel_first))
        self.bins[parallel_first] -= 1
        
        with self.stations[parallel_first].request() as req:
            yield req
            yield self.env.process(self.process_station(product_id, parallel_first, start_queue))
        
        # Second parallel station (the other one)
        parallel_second = 9 - parallel_first  # If first was 4, this is 5. if first was 5, this is 4
        start_queue = self.env.now
        
        if self.bins[parallel_second] <= 0:
            yield self.env.process(self.resupply_bin(parallel_second))
        self.bins[parallel_second] -= 1
        
        with self.stations[parallel_second].request() as req:
            yield req
            yield self.env.process(self.process_station(product_id, parallel_second, start_queue))
        
        # Quality check
        if np.random.random() < 0.05:
            self.rejected_products += 1
        else:
            self.total_production += 1

    def run_simulation(self, run_id, simulation_time):
        product_id = 0
        while self.env.now < simulation_time:
            if np.random.random() < 0.0001 / (simulation_time / 24):   # Facility accident
                print(f"Facility accident at time {self.env.now} in Run {run_id}. Stopping this simulation run.")
                break
            
            self.env.process(self.process_product(product_id))
            product_id += 1
            
            # Dynamic input rate based on Station 0 queue
            if len(self.stations[0].queue) > 5:
                yield self.env.timeout(2)  # Slow down if queue is long
            else:
                yield self.env.timeout(1)  # Normal speed otherwise

def run_simulation(seed, run_id, simulation_time):
    np.random.seed(seed)
    env = simpy.Environment()
    facility = ManufacturingFacility(env)
    env.process(facility.run_simulation(run_id, simulation_time))
    env.run(until=simulation_time)
    
    # Calculate metrics
    results = {
        'run_id': run_id,
        'production': facility.total_production,
        'rejected': facility.rejected_products,
        'supplier_occupancy': facility.supplier_busy_time / simulation_time,
        'stations': {}
    }
    
    for i, metrics in facility.metrics.items():
        results['stations'][i] = {
            'occupancy': metrics.busy_time / simulation_time,
            'downtime': metrics.downtime,
            'avg_fixing_time': np.mean(metrics.fixing_times) if metrics.fixing_times else 0,
            'avg_waiting_time': np.mean(metrics.waiting_times) if metrics.waiting_times else 0,
            'avg_bottleneck_delay': np.mean(metrics.bottleneck_delays) if metrics.bottleneck_delays else 0
        }
    
    return results

def run_simulation_per_run(num_runs, simulation_time):
    all_results = []
    random_seeds = np.random.randint(1, 1000000, size=num_runs)
    for run_id, seed in enumerate(random_seeds):
        result = run_simulation(seed, run_id, simulation_time)
        all_results.append(result)
    
    # Print per-run results
    print("\nPer-Run Simulation Results:")
    print("-" * 50)
    for result in all_results:
        print(f"\nRun {result['run_id']}:")
        print(f"  Production: {result['production']}")
        print(f"  Rejected Products: {result['rejected']}")
        print(f"  Supplier Occupancy: {result['supplier_occupancy']:.3f}")
        for station in range(6):
            print(f"  Station {station}:")
            print(f"    Occupancy Rate: {result['stations'][station]['occupancy']:.3f}")
            print(f"    Downtime: {result['stations'][station]['downtime']:.2f}")
            print(f"    Avg Fixing Time: {result['stations'][station]['avg_fixing_time']:.2f}")
            print(f"    Avg Waiting Time: {result['stations'][station]['avg_waiting_time']:.2f}")
            print(f"    Avg Bottleneck Delay: {result['stations'][station]['avg_bottleneck_delay']:.2f}")
    
    return all_results

def run_all_runs(num_runs, simulation_time):
    all_results = []
    random_seeds = np.random.randint(1, 1000000, size=num_runs)
    for run_id, seed in enumerate(random_seeds):
        result = run_simulation(seed, run_id, simulation_time)
        all_results.append(result)
    
    # Print summary statistics
    print("\nSimulation Results Summary (All Runs):")
    print("-" * 50)
    
    # Calculate averages
    productions = [r['production'] for r in all_results]
    rejections = [r['rejected'] for r in all_results]
    supplier_occs = [r['supplier_occupancy'] for r in all_results]
    
    print(f"Average Production per Run: {np.mean(productions):.2f}")
    print(f"Average Rejection Rate: {np.mean([r/(p+r) for p,r in zip(productions, rejections)]):.3f}")
    print(f"Average Supplier Occupancy: {np.mean(supplier_occs):.3f}")
    
    print("\nWorkstation Statistics (All Runs):")
    for station in range(6):
        stats = [r['stations'][station] for r in all_results]
        print(f"\nStation {station}:")
        print(f"  Occupancy Rate: {np.mean([s['occupancy'] for s in stats]):.3f}")
        print(f"  Average Downtime: {np.mean([s['downtime'] for s in stats]):.2f}")
        print(f"  Average Waiting Time: {np.mean([s['avg_waiting_time'] for s in stats]):.2f}")
        print(f"  Average Fixing Time: {np.mean([s['avg_fixing_time'] for s in stats]):.2f}")
        print(f"  Average Bottleneck Delay: {np.mean([s['avg_bottleneck_delay'] for s in stats]):.2f}")
    
    return all_results

# Example usage:
# Run 5 simulations with 5000 time units each
# run_simulation_per_run(num_runs=5, simulation_time=5000)
run_all_runs(num_runs=100, simulation_time=5000)