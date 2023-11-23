# Cloth Simulation using Spring Mass System

This project is a physics-based cloth simulation implemented using a spring mass system. It utilizes classes for "Particle" and "Spring" and builds a cloth structure using these components. The accompanying GUI allows users to interact with the cloth by dragging it around, observing its behavior based on various configurable parameters such as particle mass, spring constant, and gravity force.

## Examples

Videos of the cloth simulation with different configurations are on Google Drive.

Configuration for each video is as below:



-**[Example 1](https://drive.google.com/file/d/1K6d7FgFUokR8fpKoVTQ2RjWLgxKS6-_3/view?usp=sharing)**
```
k = 0.8, c = 0.02, g = 0.005, dt = 0.33
```
https://github.com/amireskandariii/clothsimulation/assets/129678832/94522fcd-4a5d-4a48-8e7f-55fa004015cf

-**[Example 2](https://drive.google.com/file/d/1JiLOUhBF4-KltnBbJyFDcDr07HqNQuc0/view)**
```
k = 1.2, c = 0.08, g = 0.005, dt = 0.33
```

https://github.com/amireskandariii/clothsimulation/assets/129678832/502ff523-00ab-4b45-87c5-29e297fa9323


## Features

- **Particle Class**: Represents individual particles with their position, velocity, and mass.
- **Spring Class**: Defines the connection between particles, storing spring constant, damping constant, and rest length.
- **Cloth Class**: Utilizes particles and springs to create a  grid representing cloth structure.
- **GUI Interface**: Enables users to interact with the cloth simulation and observe the cloth's response in real-time.

## Requirements

- Python 3.x
- PyOpenGL
- glfw
- numpy

## Installation

1. Clone the repository: `git clone https://github.com/amireskandariii/clothsimulation`
2. Navigate to the project directory.
3. Install requirements with `pip install -r requirements.txt` or `pip3 install -r requirements.txt`.

## Usage
0. **Configurate the cloth:**
   - Change the number of rows and columns to adjust the size of the cloth. (Line 16 and 17 in `cloth.p`)
   - Modify the spring constant and damping constant to change the cloth's rigidity. (Line 7 and 8 in `spring.py`)
   - Adjust the particle mass to change the cloth's flexibility. (Line 7 in `particle.py`)
   - Change the gravity force to observe its impact on the cloth's movement. (Line 51 in `cloth.py`)

1. **Run the simulation:**

    ```
    python3 ui.py
    ```

2. **Use the GUI interface to interact with the cloth:**
   - Drag the cloth to observe its movement.
   - Modify parameters such as particle mass, spring constant, and gravity force.
   - Observe how these changes affect the behavior of the cloth.





