import pandas as pd
from collections import deque

def round_robin_scheduling(df: pd.DataFrame, quantum: int) -> pd.DataFrame:
    """
    Round Robin scheduling algorithm with a given time quantum.

    Args:
        df (pd.DataFrame): DataFrame containing process info.
        quantum (int): Time slice for each process.

    Returns:
        pd.DataFrame: Updated DataFrame with scheduling metrics.
    """
    df = df.copy()
    df.sort_values(by="Arrival Time", inplace=True)
    df.reset_index(drop=True, inplace=True)

    n = len(df)
    remaining_time = df["Burst Time"].tolist()
    arrival_time = df["Arrival Time"].tolist()
    pid_list = df["PID"].tolist()
    priority_list = df["Priority"].tolist()

    complete = 0
    current_time = 0
    queue = deque()
    visited = [False] * n
    start_times = {}
    gantt = []

    while complete < n:
        for i in range(n):
            if arrival_time[i] <= current_time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if not queue:
            current_time += 1
            continue

        idx = queue.popleft()

        if pid_list[idx] not in start_times:
            start_times[pid_list[idx]] = current_time

        exec_time = min(quantum, remaining_time[idx])
        gantt.append((pid_list[idx], current_time, current_time + exec_time))

        current_time += exec_time
        remaining_time[idx] -= exec_time

        for i in range(n):
            if arrival_time[i] <= current_time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if remaining_time[idx] > 0:
            queue.append(idx)
        else:
            complete += 1

    metrics = []
    for pid in pid_list:
        all_executions = [(s, e) for p, s, e in gantt if p == pid]
        arrival = df.loc[df["PID"] == pid, "Arrival Time"].values[0]
        burst = df.loc[df["PID"] == pid, "Burst Time"].values[0]
        start = all_executions[0][1]
        complete_time = all_executions[-1][2]
        waiting = complete_time - arrival - burst
        turnaround = complete_time - arrival

        metrics.append({
            "PID": pid,
            "Arrival Time": arrival,
            "Burst Time": burst,
            "Priority": df.loc[df["PID"] == pid, "Priority"].values[0],
            "Start Time": start,
            "Completion Time": complete_time,
            "Waiting Time": waiting,
            "Turnaround Time": turnaround
        })

    return pd.DataFrame(metrics)
