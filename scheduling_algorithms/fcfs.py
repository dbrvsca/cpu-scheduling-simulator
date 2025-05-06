import pandas as pd

def fcfs_scheduling(df: pd.DataFrame) -> pd.DataFrame:
    """
    First-Come First-Serve scheduling algorithm.

    Args:
        df (pd.DataFrame): DataFrame containing processes with Arrival Time and Burst Time.

    Returns:
        pd.DataFrame: Updated DataFrame with Start Time, Completion Time, Waiting Time, and Turnaround Time.
    """
    df = df.copy()
    df.sort_values(by="Arrival Time", inplace=True)
    df.reset_index(drop=True, inplace=True)

    start_time = []
    completion_time = []
    waiting_time = []
    turnaround_time = []

    current_time = 0
    for index, row in df.iterrows():
        arrival = row["Arrival Time"]
        burst = row["Burst Time"]

        if current_time < arrival:
            current_time = arrival

        start = current_time
        complete = start + burst
        wait = start - arrival
        turn = complete - arrival

        start_time.append(start)
        completion_time.append(complete)
        waiting_time.append(wait)
        turnaround_time.append(turn)

        current_time = complete

    df["Start Time"] = start_time
    df["Completion Time"] = completion_time
    df["Waiting Time"] = waiting_time
    df["Turnaround Time"] = turnaround_time

    return df
