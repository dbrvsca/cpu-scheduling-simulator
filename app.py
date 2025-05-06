import streamlit as st
import pandas as pd

from utils.process_generator import generate_random_processes
from scheduling_algorithms.fcfs import fcfs_scheduling
from scheduling_algorithms.sjf import sjf_scheduling
from scheduling_algorithms.round_robin import round_robin_scheduling
from scheduling_algorithms.priority_scheduling import priority_scheduling

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

# Simulate scheduling
if st.button("Start Simulation"):
    if algorithm == "First-Come First-Serve (FCFS)":
        result_df = fcfs_scheduling(process_df)
    elif algorithm == "Shortest Job First (SJF)":
        result_df = sjf_scheduling(process_df)
    elif algorithm == "Round Robin":
        result_df = round_robin_scheduling(process_df, quantum=quantum)
    elif algorithm == "Priority Scheduling":
        result_df = priority_scheduling(process_df)
    else:
        st.error("Invalid algorithm selected.")
        result_df = None

    if result_df is not None:
        st.subheader("Simulation Result")
        st.dataframe(result_df)
