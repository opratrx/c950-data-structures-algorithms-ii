# WGUPS Routing Program

![WGUPS](https://img.shields.io/badge/WGUPS-Routing-blueviolet) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![License](https://img.shields.io/badge/License-MIT-green)

<video width="100%" controls autoplay>
  <source src="https://www.0n.engineer/swiftmd.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Overview
The **WGUPS Routing Program** is a comprehensive solution for optimizing package deliveries. This project utilizes advanced algorithms and data structures to simulate efficient routing and real-time package tracking. It ensures timely deliveries while meeting all program constraints, providing a scalable and user-friendly system for logistics operations.

---

## Features
- **Optimized Routing**: Uses a Greedy Algorithm for minimal travel time and efficient delivery planning.
- **Efficient Data Management**: Implements a Chaining Hash Table for fast and reliable storage and retrieval of package data.
- **Dynamic Delivery Simulation**: Tracks delivery status and metrics in real-time.
- **Scalable Design**: Supports increasing package loads and multiple trucks without performance degradation.
- **User-Friendly Interface**: Simplified navigation for checking statuses, viewing metrics, and managing deliveries.
- **Cross-Platform Compatibility**: Runs on macOS, Windows, and Linux environments.

---

## Table of Contents
1. [Setup](#setup)
2. [Usage](#usage)
3. [Technical Details](#technical-details)
4. [Educational Insights](#educational-insights)
5. [Examples](#examples)
6. [Future Enhancements](#future-enhancements)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)

---

## Setup
### Requirements
- **Python 3.11** or higher
- Compatible operating systems: macOS Sonoma 14.2, Windows 10/11, or Linux
- Optional: **PyCharm 2024.1 (Professional Edition)** for an enhanced development experience

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/wgups-routing.git
    cd wgups-routing
    ```
2. Install dependencies (if applicable):
    ```bash
    pip install -r requirements.txt
    ```
3. Run the program:
    ```bash
    python main.py
    ```

---

## Usage
1. Launch the program using:
    ```bash
    python main.py
    ```
2. Navigate the interactive menu to:
    - View real-time delivery status
    - Display package details
    - Check overall metrics
    - Manage truck assignments
3. Monitor delivery progress and log details for analysis.

---

## Technical Details
### Algorithms
- **Greedy Algorithm**: Iteratively selects the closest delivery point, ensuring efficiency and simplicity.
- **Chaining Hash Table**: Handles package data with average-case $O(1)$ operations for search, insertion, and deletion.

### Key Components
- **Package Class**: Manages package data (ID, address, deadline, weight, status).
- **Truck Class**: Simulates truck behavior, including capacity and route management.
- **Distance Matrix**: Preloaded with delivery point distances for quick lookups.

### Complexity Analysis
- **Greedy Algorithm**: $O(n^2)$ for nested iterations over delivery points.
- **Hash Table Operations**: Average-case $O(1)$; worst-case $O(n)$ for high collision scenarios.

---

## Educational Insights
### 1. Greedy Algorithm for Routing
#### Code Snippet:
```python
# Greedy Algorithm Implementation
for package in package_list:
    nearest_package = min(remaining_packages, key=lambda p: distance_matrix[current_location][p.address])
    route.append(nearest_package)
    current_location = nearest_package.address
    remaining_packages.remove(nearest_package)
```
#### Explanation:
- The algorithm calculates the distance from the current location to all remaining delivery points.
- Selects the nearest point and updates the route iteratively.
- Time complexity: $O(n^2)$ due to nested loops for distance comparisons.

### 2. Chaining Hash Table
#### Code Snippet:
```python
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, key, value):
        index = hash(key) % self.size
        self.table[index].append((key, value))

    def lookup(self, key):
        index = hash(key) % self.size
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
```
#### Explanation:
- Efficiently stores and retrieves package data using hash functions.
- Resolves collisions with linked lists (chaining).
- Operations: Average $O(1)$, Worst $O(n)$.

### 3. Truck Metrics Logging
#### Code Snippet:
```python
def log_truck_metrics_with_date(truck, truck_num):
    print(f"Truck {truck_num} Total Distance: {truck.total_distance}")
    print(f"Truck {truck_num} Delivery Time: {truck.delivery_time}")
```
#### Explanation:
- Logs key metrics for each truck, such as total distance and delivery time.
- Simple $O(1)$ operation per log.

### 4. Console Color Class
#### Code Snippet:
```python
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    RESET = "\033[0m"

def print_success(message):
    print(f"{Colors.GREEN}{message}{Colors.RESET}")
```
#### Explanation:
- Provides ANSI color codes for console output, improving readability and user experience.

---

## Examples
### Delivery Simulation
#### Example Status Checks:
```plaintext
9:00 AM:
Package 1: Delivered
Package 2: In Transit

10:15 AM:
Package 1: Delivered
Package 2: Delivered

12:30 PM:
All packages delivered successfully.
```


---

## Future Enhancements
- Implement **Dijkstra’s Algorithm** for shortest path routing.
- Add support for **dynamic delivery depots** and multi-hub logistics.
- Introduce a **visual mapping interface** for real-time route visualization.
- Modularize the codebase for easier updates and maintenance.
- Explore advanced data structures like **graphs** for enhanced delivery modeling.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- **WGU Faculty**: For their guidance and resources.
- **GeeksforGeeks**: For insights into algorithm optimizations.
- **Python Community**: For providing robust libraries and tools for development.
- **Nagaraj (2023)**: For insights on advanced algorithms like Dijkstra’s.

