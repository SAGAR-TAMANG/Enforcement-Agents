# 🛡️ Enforcement Agents: Real-Time Oversight in Multi-Agent Systems

This repository contains the official simulation code for the **Enforcement Agent (EA) Framework**, a novel approach to achieving safety and alignment in multi-agent environments through embedded real-time supervision.

The simulation is built in a custom 2D drone environment using [Gymnasium](https://github.com/Farama-Foundation/Gymnasium), where drones patrol a protected zone while identifying and neutralizing incoming threats. The twist? Some drones are **malicious**—and only **Enforcement Agents (EAs)** can identify and reform them during runtime.

---

## 📁 Repository Structure

- `main.py`: Core simulation environment (`DroneMASGame`), rendering logic, and EA reformation flow.
- `runner.py`: Batch simulation runner that executes multiple trials, logs CSV summaries, and auto-generates screenshots.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/SAGAR-TAMANG/Enforcement-Agents.git
cd Enforcement-Agents
```

### 2. Install Dependencies

Make sure Python 3.8+ is installed.

```bash
pip install gymnasium matplotlib numpy
```

### 3. Run a Single Simulation

This launches an interactive simulation where you can visually inspect drone and enemy movements.

```bash
python main.py
```

### 4. Run Batch Simulations + Export CSV

This runs 30 simulations each:
- Without EA (`results_no_ea.csv`)
- With 1 EA (`results_with_ea.csv`)
- Optionally, add a third run for 2 EAs (`results_with_2_ea.csv`)

```bash
python runner.py
```

Make sure the `screenshots/` folder exists to store PNGs.

---

## 📊 Research Context

This project supports the findings in the research paper titled:

> **"Enforcement Agents: Real-Time Supervision in Multi-Agent Environments"**

All final tables and visual outcomes can be found in the `appendix` and `results/` folders respectively.

---