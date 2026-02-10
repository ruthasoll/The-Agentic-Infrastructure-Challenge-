"""
Campaign Management Page

SRS Reference: §4.6 Orchestration, FR6.1 (Campaign Lifecycle)
Spec: specs/frontend.md, UI1

Allows operators to create new campaigns and view existing ones.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(page_title="Campaigns", page_icon="📢", layout="wide")

st.title("📢 Campaign Management")

# --- Create Campaign Form ---
with st.expander("Create New Campaign", expanded=False):
    with st.form("campaign_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Campaign Name", placeholder="e.g. Summer Launch")
            goal = st.text_area("Campaign Goal", placeholder="Describe the objective...")
            
        with col2:
            budget = st.number_input("Budget (USD)", min_value=100.0, value=1000.0, step=100.0)
            platforms = st.multiselect("Platforms", ["Twitter", "Instagram", "TikTok", "LinkedIn"], default=["Twitter"])
            
        submit = st.form_submit_button("Launch Campaign 🚀")
        
        if submit:
            if not name or not goal:
                st.error("Please provide a name and goal.")
            else:
                # Mock backend call
                campaign_id = str(uuid.uuid4())
                st.success(f"Campaign '{name}' launched successfully! ID: {campaign_id}")
                st.balloons()

# --- Active Campaigns Table ---
st.subheader("Active Campaigns")

# Mock data
campaigns = [
    {
        "ID": "101",
        "Name": "Q3 Brand Awareness",
        "Status": "Running",
        "Progress": 65,
        "Budget Used": "$3,200 / $5,000",
        "Agents": 3
    },
    {
        "ID": "102",
        "Name": "Product Launch Alpha",
        "Status": "Planning",
        "Progress": 10,
        "Budget Used": "$0 / $2,000",
        "Agents": 1
    },
    {
        "ID": "103",
        "Name": "Community Engagement",
        "Status": "Completed",
        "Progress": 100,
        "Budget Used": "$1,500 / $1,500",
        "Agents": 0
    }
]

df = pd.DataFrame(campaigns)

# Styled dataframe
st.dataframe(
    df,
    column_config={
        "Progress": st.column_config.ProgressColumn(
            "Progress",
            help="Campaign completion percentage",
            format="%d%%",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    use_container_width=True
)

# --- Task View ---
st.subheader("Task Breakdown")
selected_campaign = st.selectbox("Select Campaign", [c["Name"] for c in campaigns])

if selected_campaign == "Q3 Brand Awareness":
    tasks = [
        {"Task": "Fetch Trends", "Agent": "worker-01", "Status": "✅ Done"},
        {"Task": "Generate Content", "Agent": "worker-02", "Status": "🔄 In Progress"},
        {"Task": "Review Content", "Agent": "judge-01", "Status": "⏳ Pending"},
    ]
    st.table(tasks)
elif selected_campaign == "Product Launch Alpha":
    st.info("Planning in progress. No tasks assigned yet.")
else:
    st.success("All tasks completed.")
