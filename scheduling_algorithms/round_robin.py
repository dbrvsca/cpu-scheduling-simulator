import pandas as pd
from collections import deque

def round_robin_scheduling(df: pd.DataFrame, quantum: int) -> tuple[pd.DataFrame, list]:
    """
    Round Robin scheduling algorithm with time quantum.

    Returns both the metrics DataFrame and the Gantt chart data.
    """
    df = df.copy()
    df.sort_values(by="Arrival Time", inplace=True)
    df.reset_index(drop=True, inplace=True)

    n = len(df)
    remaining_time = df["Burst Time"].tolist()
    arrival_time = df["Arrival Time"].tolist()
    pid_list = df["PID"].tolist()

    complete = 0
    current_time = 0
    queue = deque()
    visited = [False] * n
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
        all_executions = [(s, e) for (p, s, e) in gantt if p == pid]
        if all_executions:
            start = all_executions[0][0]
            complete_time = all_executions[-1][1]
        else:
            start = 0
            complete_time = 0

        arrival = df.loc[df["PID"] == pid, "Arrival Time"].values[0]
        burst = df.loc[df["PID"] == pid, "Burst Time"].values[0]
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

    return pd.DataFrame(metrics), gantt