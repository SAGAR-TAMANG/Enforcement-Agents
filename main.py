# Full working code for DroneMASGame with Enforcement Agents, success/failure logging, and final report

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time


class DroneMASGame(gym.Env):
    def __init__(self, render_mode=None, map_size=120, num_drones=5, num_enemies=1,
                 detection_radius=10, center_radius=5, num_enforcement_agents=0, render_fps=120):
        super(DroneMASGame, self).__init__()
        
        self.pause_on_end = True
        self.map_size = map_size
        self.num_drones = num_drones
        self.num_enemies = num_enemies
        self.detection_radius = detection_radius
        self.center_radius = center_radius
        self.num_enforcement_agents = num_enforcement_agents
        self.enemies_spawn_interval = 15
        self.steps = 0
        self.start_time = None
        self.end_time = None
        self.metadata = {"render_modes": ["human"], "render_fps": render_fps}

        self.center = np.array([map_size // 2, map_size // 2])
        self.drone_angles = np.linspace(0, 2 * np.pi, num_drones, endpoint=False)
        self.drone_radius_levels = np.random.randint(20, 30, size=num_drones)

        self.ea_angles = np.linspace(0, 2 * np.pi, num_enforcement_agents, endpoint=False)
        self.ea_radius_levels = np.random.randint(18, 27, size=num_enforcement_agents)
        self.ea_positions = []

        # For final reporting
        self.episode_result = None
        self.final_steps = 0
        self.final_duration_sec = 0.0
        self.num_healthy_drones = 0
        self.num_malicious_drones = 0
        self.num_enforcement_agents_final = self.num_enforcement_agents
        self.num_reformed_drones = 0

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Dict({
            "drones": spaces.Box(0, map_size, shape=(num_drones, 2), dtype=np.int32),
            "enemies": spaces.Box(0, map_size, shape=(num_enemies, 2), dtype=np.int32)
        })

        self.fig, self.ax = None, None
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.steps = 0
        self.start_time = time.time()
        self.enemies = []
        self.malicious_drones = random.sample(range(self.num_drones), k=max(1, self.num_drones // 5))

        self.drones = []
        for i in range(self.num_drones):
            angle = self.drone_angles[i]
            r = self.drone_radius_levels[i]
            x = int(self.center[0] + r * np.cos(angle)) % self.map_size
            y = int(self.center[1] + r * np.sin(angle)) % self.map_size
            self.drones.append([x, y])
        self.drones = np.array(self.drones)

        self.ea_positions = []
        for i in range(self.num_enforcement_agents):
            angle = self.ea_angles[i]
            r = self.ea_radius_levels[i]
            x = int(self.center[0] + r * np.cos(angle)) % self.map_size
            y = int(self.center[1] + r * np.sin(angle)) % self.map_size
            self.ea_positions.append([x, y])
        self.ea_positions = np.array(self.ea_positions)

        # Reset final state tracking
        self.episode_result = None
        self.final_steps = 0
        self.final_duration_sec = 0.0
        self.num_malicious_drones = len(self.malicious_drones)
        self.num_healthy_drones = self.num_drones - self.num_malicious_drones

        return self._get_obs(), {}

    def _get_obs(self):
        return {
            "drones": self.drones.copy(),
            "enemies": np.array(self.enemies)
        }

    def _distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2))

    def _spawn_enemy(self):
        side = random.choice([0, 1, 2, 3])
        if side == 0:
            x, y = random.randint(0, self.map_size), 0
        elif side == 1:
            x, y = random.randint(0, self.map_size), self.map_size
        elif side == 2:
            x, y = 0, random.randint(0, self.map_size)
        else:
            x, y = self.map_size, random.randint(0, self.map_size)
        self.enemies.append([x, y])

    def step(self, actions):
        self.steps += 1

        for i in range(self.num_drones):
            self.drone_angles[i] += 0.05
            angle = self.drone_angles[i]
            r = self.drone_radius_levels[i]
            x = int(self.center[0] + r * np.cos(angle)) % self.map_size
            y = int(self.center[1] + r * np.sin(angle)) % self.map_size
            self.drones[i] = [x, y]

        for i in range(self.num_enforcement_agents):
            self.ea_angles[i] -= 0.05
            angle = self.ea_angles[i]
            r = self.ea_radius_levels[i]
            x = int(self.center[0] + r * np.cos(angle)) % self.map_size
            y = int(self.center[1] + r * np.sin(angle)) % self.map_size
            self.ea_positions[i] = [x, y]

        for enemy in self.enemies:
            direction = self.center - np.array(enemy)
            step = direction / (np.linalg.norm(direction) + 1e-5)
            enemy[0] += int(np.round(step[0] * 1.0))
            enemy[1] += int(np.round(step[1] * 1.0))

        new_enemies = []
        for enemy in self.enemies:
            detected = False
            for i, drone in enumerate(self.drones):
                if self._distance(drone, enemy) <= self.detection_radius:
                    if i not in self.malicious_drones:
                        detected = True
                        break
            if not detected:
                new_enemies.append(enemy)
        self.enemies = new_enemies

        for i, ea in enumerate(self.ea_positions):
            for j, drone in enumerate(self.drones):
                if j in self.malicious_drones:
                    if self._distance(ea, drone) <= self.detection_radius:
                        for enemy in self.enemies:
                            if self._distance(drone, enemy) <= self.detection_radius:
                                self.malicious_drones.remove(j)
                                self.num_reformed_drones += 1
                                break

        if self.steps % self.enemies_spawn_interval == 0:
            self._spawn_enemy()

        for enemy in self.enemies:
            if self._distance(enemy, self.center) <= self.center_radius:
                self.end_time = time.time()
                self.final_duration_sec = self.end_time - self.start_time
                self.final_steps = self.steps
                self.episode_result = "fail"
                if self.fig and self.ax:
                    self.ax.text(5, 5, f"Episode Ended — Threat Reached Center\nSimulation Steps: {self.final_steps}\nElapsed Time: {self.final_duration_sec:.2f}s",
                                 fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.8))
                    if hasattr(self, "screenshot_path") and self.fig:
                        self.fig.savefig(self.screenshot_path, dpi=300, bbox_inches='tight')
                    if self.pause_on_end:
                        plt.pause(3)
                return self._get_obs(), -100, True, False, {"reason": "enemy_reached_center"}

        if self.steps >= 1200:
            self.end_time = time.time()
            self.final_duration_sec = self.end_time - self.start_time
            self.final_steps = self.steps
            self.episode_result = "success"
            if self.fig and self.ax:
                self.ax.text(5, 5,
                             f"Episode Completed — No Breach Detected\nSimulation Steps: {self.final_steps}\nTotal Duration: {self.final_duration_sec:.2f}s",
                             fontsize=10, color='black', bbox=dict(facecolor='lightgreen', alpha=0.8))
                if hasattr(self, "screenshot_path") and self.fig:
                    self.fig.savefig(self.screenshot_path, dpi=300, bbox_inches='tight')
                if self.pause_on_end:
                    plt.pause(3)
            return self._get_obs(), 100, True, False, {"reason": "simulation_success"}

        return self._get_obs(), 0, False, False, {}

    def render(self):
        fps = self.metadata.get("render_fps", 120)
        
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.clear()

        self.ax.set_xlim(0, self.map_size)
        self.ax.set_ylim(0, self.map_size)

        # Protected center
        center_circle = patches.Circle(self.center, self.center_radius, color='yellow', alpha=0.5, label='Protected Center')
        self.ax.add_patch(center_circle)

        for i, drone in enumerate(self.drones):
            if i in self.malicious_drones:
                self.ax.plot(drone[0], drone[1], 'rx', markersize=10,
                            label='Malicious Drone' if i == self.malicious_drones[0] else "")
                circle = patches.Circle(drone, self.detection_radius, color='red', fill=False, linestyle='--', alpha=0.3)
                self.ax.add_patch(circle)
            else:
                self.ax.plot(drone[0], drone[1], 'bo',
                            label='Drone' if i == 0 else "")
                circle = patches.Circle(drone, self.detection_radius, color='blue', fill=False, linestyle='--', alpha=0.3)
                self.ax.add_patch(circle)

        for i, ea in enumerate(self.ea_positions):
            self.ax.plot(ea[0], ea[1], 'gs', markersize=8,
                        label='Enforcement Agent' if i == 0 else "")
            circle = patches.Circle(ea, self.detection_radius, color='green', fill=False, linestyle='--', alpha=0.3)
            self.ax.add_patch(circle)

        for i, enemy in enumerate(self.enemies):
            self.ax.plot(enemy[0], enemy[1], 'ro',
                        label='Enemy' if i == 0 else "")

        self.ax.set_title(f"Step: {self.steps}")
        self.ax.legend(loc='upper right')
        plt.pause(1 / fps)
        plt.draw()

    def close(self):
        if self.fig:
            plt.close(self.fig)

if __name__ == "__main__":
    env = DroneMASGame(num_drones=6, num_enforcement_agents=1)
    obs, _ = env.reset()

    done = False
    while not done:
        actions = [0] * env.num_drones
        obs, reward, done, _, info = env.step(actions)
        env.render()
    env.close()

    print("✅ Final Episode Summary")
    print("Result:", env.episode_result)
    print("Steps:", env.final_steps)
    print("Duration (s):", f"{env.final_duration_sec:.2f}")
    print("Healthy Drones:", env.num_healthy_drones)
    print("Malicious Drones:", env.num_malicious_drones)
    print("Enforcement Agents:", env.num_enforcement_agents_final)
    print("Reformed Malicious Drones:", env.num_reformed_drones)