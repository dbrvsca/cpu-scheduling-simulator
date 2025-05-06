import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Patch



def plot_gantt_chart(gantt: list) -> plt.Figure:
    """
    Generate a Gantt chart from the list of execution tuples (pid, start, end).
    """
    fig, ax = plt.subplots(figsize=(10, 2 + len(set(p for p, _, _ in gantt)) * 0.5))

    unique_pids = list(dict.fromkeys(p for p, _, _ in gantt))
    colors = sns.color_palette("tab10", len(unique_pids))
    pid_to_color = {pid: colors[i % len(colors)] for i, pid in enumerate(unique_pids)}

    for pid, start, end in gantt:
        ax.barh(pid, end - start, left=start, color=pid_to_color[pid])
        ax.text(start + 0.1, pid, f"{start}→{end}", va='center', ha='left', fontsize=8)

    ax.set_xlabel("Time")
    ax.set_ylabel("Process")
    ax.set_title("Gantt Chart")
    ax.grid(True)
    return fig

def plot_metric_bars(df: pd.DataFrame) -> plt.Figure:
    """
    Plot bar chart of Waiting Time and Turnaround Time per process.

    Args:
        df (pd.DataFrame): DataFrame with metrics per process.

    Returns:
        plt.Figure: Bar chart comparing metrics.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_width = 0.35
    x = range(len(df))

    ax.bar(x, df["Waiting Time"], width=bar_width, label="Waiting Time", color="skyblue")
    ax.bar([i + bar_width for i in x], df["Turnaround Time"], width=bar_width, label="Turnaround Time", color="lightgreen")

    ax.set_xlabel("Processes")
    ax.set_ylabel("Time")
    ax.set_title("Process Metrics Comparison")
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(df["PID"].tolist())
    ax.legend()

    return fig
