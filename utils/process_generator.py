
import random
import pandas as pd

def generate_random_processes(n: int, seed: int = None) -> pd.DataFrame:
    """
    Generate n random processes with arrival time, burst time, and priority.

    Args:
        n (int): Number of processes to generate.
        seed (int, optional): Random seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame with columns: PID, Arrival Time, Burst Time, Priority.
    """
    
    if seed is not None:
        random.seed(seed)

    processes = []
    for i in range(n):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        priority = random.randint(1, 5)
        processes.append({
            "PID": f"P{i+1}",
            "Arrival Time": arrival_time,
            "Burst Time": burst_time,
            "Priority": priority
        })

    df = pd.DataFrame(processes)
    df.sort_values(by="Arrival Time", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_example_manual_processes() -> pd.DataFrame:
    """
    Returns a sample manually defined process list for testing.

    Returns:
        pd.DataFrame: DataFrame of sample processes.
    """
    data = [
        {"PID": "P1", "Arrival Time": 0, "Burst Time": 5, "Priority": 2},
        {"PID": "P2", "Arrival Time": 2, "Burst Time": 3, "Priority": 1},
        {"PID": "P3", "Arrival Time": 4, "Burst Time": 1, "Priority": 3},
        {"PID": "P4", "Arrival Time": 5, "Burst Time": 2, "Priority": 2},
        {"PID": "P5", "Arrival Time": 6, "Burst Time": 4, "Priority": 1},
    ]
    return pd.DataFrame(data)
