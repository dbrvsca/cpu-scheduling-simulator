import pandas as pd

def calculate_summary_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate average waiting time, turnaround time, and CPU utilization.

    Args:
        df (pd.DataFrame): Scheduling result with necessary columns.

    Returns:
        dict: Summary metrics.
    """
    avg_waiting_time = df["Waiting Time"].mean()
    avg_turnaround_time = df["Turnaround Time"].mean()

    total_burst = df["Burst Time"].sum()
    makespan = df["Completion Time"].max() - df["Arrival Time"].min()
    cpu_utilization = (total_burst / makespan) * 100 if makespan else 0

    return {
        "Average Waiting Time": round(avg_waiting_time, 2),
        "Average Turnaround Time": round(avg_turnaround_time, 2),
        "CPU Utilization (%)": round(cpu_utilization, 2)
    }