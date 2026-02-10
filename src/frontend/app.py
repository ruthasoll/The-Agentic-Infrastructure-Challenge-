"""
Application Entry Point: Agent Command Center

SRS Reference: §4.6 Orchestration, FR6.3
Spec: specs/frontend.md

Main dashboard layout and navigation.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

st.set_page_config(
    page_title="Project Chimera",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🤖 Project Chimera: Command Center")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Active Campaigns", value="3", delta="1")
    
    with col2:
        st.metric(label="Agents Online", value="5", delta="0")
        
    with col3:
        st.metric(label="24h Spend", value="$124.50", delta="-12%")
        
    st.markdown("---")
    
    st.subheader("System Health")
    st.info("✅ All systems operational. MCP Gateway Connected.")
    
    st.subheader("Recent Activity")
    activity_data = [
        {"timestamp": "10:45 AM", "agent": "worker-01", "event": "Published post to Twitter"},
        {"timestamp": "10:42 AM", "agent": "planner-01", "event": "Decomposed Campaign #102"},
        {"timestamp": "10:30 AM", "agent": "judge-01", "event": "Approved content #554"},
    ]
    st.table(activity_data)

if __name__ == "__main__":
    main()
