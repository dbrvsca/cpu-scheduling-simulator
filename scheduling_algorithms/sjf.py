import pandas as pd

def sjf_scheduling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Shortest Job First scheduling algorithm.
    """

    df = df.copy()
    df.sort_values(by="Arrival Time", inplace=True)
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
    
        idx = ready_queue["Burst Time"].idxmin()
        row = df.loc[idx]
        arrival = row["Arrival Time"]
        burst = row["Burst Time"]

        start = current_time
        complete = start + burst
        wait = start - arrival
        turn = complete - arrival

        result.append({
            "PID": row["PID"],
            "Arrival Time": arrival,
            "Burst Time": burst,
            "Priority": row["Priority"],
            "Start Time": start,
            "Completion Time": complete,
            "Waiting Time": wait,
            "Turnaround Time": turn
        })

        current_time = complete
        visited[idx] = True
        completed += 1

    return pd.DataFrame(result)
