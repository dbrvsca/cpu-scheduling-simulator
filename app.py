import streamlit as st
import pandas as pd

from utils.process_generator import generate_random_processes
from scheduling_algorithms.fcfs import fcfs_scheduling
from scheduling_algorithms.sjf import sjf_scheduling
from scheduling_algorithms.round_robin import round_robin_scheduling
from scheduling_algorithms.priority_scheduling import priority_scheduling
from utils.visualisation import plot_gantt_chart, plot_metric_bars
from utils.metrics import calculate_summary_metrics

# Title
st.title("CPU Scheduling Algorithm Simulator")

# Sidebar: Algorithm selection and settings
st.sidebar.header("Simulation Settings")
algorithm = st.sidebar.selectbox(
    "Choose Scheduling Algorithm",
    ("First-Come First-Serve (FCFS)", "Shortest Job First (SJF)", "Round Robin", "Priority Scheduling")
)

num_processes = st.sidebar.slider("Number of processes", 3, 15, 5)
random_seed = st.sidebar.number_input("Random seed (optional)", value=42)
quantum = None
if algorithm == "Round Robin":
    quantum = st.sidebar.slider("Quantum (Time Slice)", 1, 10, 3)

# Generate data
process_df = generate_random_processes(num_processes, seed=random_seed)
st.subheader("Generated Process Table")
st.dataframe(process_df)

# Initialize result_df and gantt
result_df = None

gantt = []

# Simulate scheduling
if st.button("Start Simulation"):
    if algorithm == "First-Come First-Serve (FCFS)":
        result_df = fcfs_scheduling(process_df)
    elif algorithm == "Shortest Job First (SJF)":
        result_df = sjf_scheduling(process_df)
    elif algorithm == "Round Robin":
        result_df, gantt = round_robin_scheduling(process_df, quantum=quantum)
    elif algorithm == "Priority Scheduling":
        result_df = priority_scheduling(process_df)

    if result_df is not None:
        st.subheader("Simulation Result")
        st.dataframe(result_df)

        if algorithm == "Round Robin":
            st.subheader("Gantt Chart")
            gantt_fig = plot_gantt_chart(gantt)
            st.pyplot(gantt_fig)
        else:
            gantt_fig = plot_gantt_chart(
                [(row["PID"], row["Start Time"], row["Completion Time"]) for _, row in result_df.iterrows()]
            )
            st.subheader("Gantt Chart")
            st.pyplot(gantt_fig)

        st.subheader("Metrics Comparison")
        metrics_fig = plot_metric_bars(result_df)
        st.pyplot(metrics_fig)

        st.subheader("Summary Metrics")
        metrics = calculate_summary_metrics(result_df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Waiting Time", f"{metrics['Average Waiting Time']} units")
        col2.metric("Avg Turnaround Time", f"{metrics['Average Turnaround Time']} units")
        col3.metric("CPU Utilization", f"{metrics['CPU Utilization (%)']}%")