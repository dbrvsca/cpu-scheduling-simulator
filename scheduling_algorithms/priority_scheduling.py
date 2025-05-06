import pandas as pd

def priority_scheduling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Non-preemptive Priority Scheduling algorithm.

    Args:
        df (pd.DataFrame): Input DataFrame containing processes.

    Returns:
        pd.DataFrame: Updated DataFrame with scheduling results.
    """
    df = df.copy()
    df.sort_values(by=["Arrival Time"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    completed = 0
    current_time = 0
    visited = [False] * len(df)
    result = []

    while completed < len(df):
        ready_queue = df[(df["Arrival Time"] <= current_time) & (~pd.Series(visited))]
        if ready_queue.empty:
            current_time += 1
            continue

        idx = ready_queue["Priority"].idxmin()
        row = df.loc[idx]
        arrival = row["Arrival Time"]
        burst = row["Burst Time"]
        priority = row["Priority"]

        start = current_time
        complete = start + burst
        wait = start - arrival
        turn = complete - arrival

        result.append({
            "PID": row["PID"],
            "Arrival Time": arrival,
            "Burst Time": burst,
            "Priority": priority,
            "Start Time": start,
            "Completion Time": complete,
            "Waiting Time": wait,
            "Turnaround Time": turn
        })

        current_time = complete
        visited[idx] = True
        completed += 1

    return pd.DataFrame(result)
