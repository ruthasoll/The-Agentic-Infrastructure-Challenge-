"""
Agent Monitor Page

SRS Reference: §4.6 Orchestration, FR6.3 (Telemetry)
Spec: specs/frontend.md, UI2

Real-time view of agent status and health.
"""

import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Agents", page_icon="🤖", layout="wide")

st.title("🤖 Agent Fleet Monitor")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Agents", "5")
col2.metric("Active", "3", delta="Running Tasks")
col3.metric("Idle", "2")
col4.metric("Errors (24h)", "0", delta_color="normal")

st.markdown("---")

# Agent Grid
agents = [
    {"name": "planner-01", "role": "Planner", "status": "Busy", "task": "Decomposing Campaign #102", "health": 100},
    {"name": "worker-01", "role": "Worker", "status": "Busy", "task": "Generating Image for #101", "health": 98},
    {"name": "worker-02", "role": "Worker", "status": "Idle", "task": "-", "health": 100},
    {"name": "judge-01", "role": "Judge", "status": "Busy", "task": "Reviewing Content #554", "health": 100},
    {"name": "orchestrator", "role": "System", "status": "Active", "task": "Monitoring Swarm", "health": 100},
]

# Display as cards
cols = st.columns(3)
for i, agent in enumerate(agents):
    with cols[i % 3]:
        with st.container(border=True):
            st.subheader(f"{agent['name']}")
            st.caption(f"Role: **{agent['role']}**")
            
            if agent['status'] == "Busy":
                st.warning(f"Constructing... ({agent['task']})")
                st.progress(70)
            elif agent['status'] == "Active":
                st.success("Operational")
            else:
                st.info("Waiting for tasks")
                
            st.metric("Health", f"{agent['health']}%")

# Telemetry Log
st.subheader("Live Telemetry Stream")
logs = [
    "2023-10-27 10:45:12 [INFO] worker-01: Task claimed (ID: task-123)",
    "2023-10-27 10:45:15 [INFO] worker-01: Generating constraints...",
    "2023-10-27 10:45:18 [INFO] judge-01: Content received for review",
    "2023-10-27 10:45:20 [WARN] planner-01: Budget proximity alert (85%)",
]
st.code("\n".join(logs), language="text")
