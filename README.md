# **Project I: The Manufacturing Facility**  

This project is a **discrete-event simulation** of a **manufacturing facility** that produces electronic devices, designed using **Python and SimPy**. The simulation models **six workstations**, raw material resupply, machine failures, bottlenecks, and quality control, allowing for **statistical analysis and optimization of the production process**.  

## **Key Features**  
- **Six Workstations with Sequential Processing**: Products move through six stations, with **parallel processing at stations 4 and 5**.  
- **Raw Material Management**: Each workstation has a **limited bin (25 units)**, automatically resupplied by **three supplier devices**, with a **normal distribution delay**.  
- **Workstation Performance & Failures**: Each station has a **failure probability**, with **predictive maintenance at station 3** and **regular maintenance every 5 products elsewhere**.  
- **Production Uncertainties**: The simulation includes **random product rejections (5%)** and **facility-wide accidents (1%)** that can halt production.  
- **Dynamic Input Rate**: If the queue at station 0 exceeds five items, the system **slows down** to prevent overloading.  
- **Performance Metrics Tracked Per Run**:  
  - **Final production output**  
  - **Rejection rate**  
  - **Workstation occupancy and downtime**  
  - **Supplier device utilization**  
  - **Fixing times and bottleneck delays**  

## **Simulation Execution**  
- The system **runs 100 independent simulations**, each lasting **5000 time units**, to gather statistical insights.  
- **Random seeds** ensure variability, mimicking real-world uncertainties.  
- **Final Analysis & Recommendations**: The results provide insights into factory efficiency, bottlenecks, and potential improvements, such as **adjusting bin sizes, increasing supplier capacity, or improving machine reliability**.  

## **Implementation Details**  
- **Developed in Python with SimPy** for event-driven modeling.  
- **Fully parameterized** to allow easy modifications and testing of different scenarios.  
- **Comprehensive Report**: Includes data-driven recommendations for improving factory performance based on simulation results.  

This project applies **discrete-event simulation, stochastic modeling, and performance analysis** to optimize **manufacturing efficiency** and **decision-making** in industrial environments.
