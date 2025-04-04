# Drone Surveillance Multi-Agent System

This project implements a simulation of a multi-agent drone surveillance system using Gymnasium (formerly OpenAI Gym). The simulation demonstrates concepts of agent cooperation, malicious agents, and enforcement agents in a security scenario.

## Overview

The simulation models a 2D environment where drones patrol to protect a central zone. Enemies periodically spawn at the edges of the map and try to reach the protected central zone. Regular drones detect and eliminate enemies, while malicious drones secretly aid the enemies. Optional enforcement agents (police drones) can detect and eliminate malicious drones.

## Features

- **Multi-agent system**: Drones communicate and coordinate to optimize coverage
- **Adversarial dynamics**: Some drones are secretly malicious and help the enemies
- **Enforcement agents**: Optional police drones that investigate and eliminate malicious drones
- **Visual interface**: Real-time 2D visualization of the environment
- **Data collection**: Statistics tracking and chart generation for research purposes
- **Configurable parameters**: Adjustable drone numbers, speeds, detection ranges, etc.

## File Structure

- `drone_surveillance_game.py`: Main environment implementation
- `main.py`: Command-line interface to run simulations

## Requirements

- Python 3.7+
- Gymnasium
- NumPy
- Pygame
- Matplotlib

## Installation

```bash
pip install gymnasium numpy pygame matplotlib
```

## Usage

### Basic Usage

```bash
python main.py
```

This runs a standard simulation with default parameters.

### Command-line Options

```bash
python main.py --mode compare --episodes 5 --drones 8 --malicious 3 --enforcement 2
```

Available modes:
- `standard`: Run without enforcement agents
- `enforcement`: Run with enforcement agents
- `compare`: Run both and generate comparison charts

Other parameters:
- `--episodes`: Number of episodes to run
- `--steps`: Maximum steps per episode
- `--drones`: Number of regular drones
- `--malicious`: Number of malicious drones
- `--enforcement`: Number of enforcement agents
- `--no-render`: Disable rendering for faster simulations
- `--map-size`: Size of the map

## Research Application

This simulation provides a testbed for studying:

1. **Multi-agent coordination**: How drones optimize their positions for maximum coverage
2. **Adversarial behavior**: Detection and mitigation of malicious agents
3. **Enforcement efficacy**: Impact of enforcement agents on system performance
4. **Resilience metrics**: How system performance degrades with increasing numbers of malicious agents

## Visualization

The system generates charts showing:
- Steps per game
- Enemy success rate
- Average coverage of the protected zone
- Enemy and malicious drone statistics

## Example Agent Implementations

- `RandomAgent`: Takes random actions
- `ProtectiveAgent`: Implements a basic protection strategy

You can extend the system by implementing more sophisticated agent strategies.

## Extending the System

To implement your own agent, create a class with an `act(observation)` method that returns actions for all drones based on the current observation.

## Author

This simulation was developed for research purposes in multi-agent systems with enforcement agents.