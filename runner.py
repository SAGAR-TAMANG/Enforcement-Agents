from main import DroneMASGame

import csv
import os

# Function to run multiple simulations and save results to CSV
def run_simulations_and_log(num_runs=50, num_drones=6, num_enforcement_agents=1, csv_file="simulation_results.csv"):
    # Check if file exists, if not create with headers
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header if needed
        if not file_exists:
            writer.writerow([
                "Run", "EA_Count", "Result", "Steps", "Duration_sec",
                "Healthy_Drones", "Malicious_Drones", "Reformed_Drones"
            ])

        for run in range(1, num_runs + 1):
            env = DroneMASGame(num_drones=num_drones, num_enforcement_agents=num_enforcement_agents, render_fps=120)
            # Assign screenshot filename to env instance
            env.screenshot_path = f"screenshots/{os.path.splitext(csv_file)[0]}_run_{run:03d}.png"
            env.pause_on_end = False
            
            obs, _ = env.reset()


            done = False
            while not done:
                actions = [0] * env.num_drones  # auto-move drones
                obs, reward, done, _, info = env.step(actions)
                env.render()  # 👈 THIS is the reason you see one visual
            env.close()

            # Write results
            writer.writerow([
                run,
                env.num_enforcement_agents_final,
                env.episode_result,
                env.final_steps,
                round(env.final_duration_sec, 2),
                env.num_healthy_drones,
                env.num_malicious_drones,
                env.num_reformed_drones
            ])

    print(f"✅ {num_runs} simulations completed and saved to '{csv_file}'.")

# Example usage: run 30 simulations with and without EA
# run_simulations_and_log(num_runs=30, num_enforcement_agents=0, csv_file="results_no_ea.csv")
run_simulations_and_log(num_runs=30, num_enforcement_agents=2, csv_file="results_with_2_ea.csv")