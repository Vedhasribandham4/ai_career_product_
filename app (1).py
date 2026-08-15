import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerPilot AI")
st.caption("Your AI Career Copilot")

# Sidebar Navigation
st.sidebar.title("🚀 CareerPilot AI")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "👤 Career Profile",
        "🔎 Opportunity Radar",
        "📄 Resume & Outreach",
        "🧠 Skill Gap Analyzer",
        "🗺️ Career Roadmap",
        "📋 Application Tracker",
        "🎤 Interview Coach",
        "💡 Product Builder"
    ]
)

# Page Routing
if page == "🏠 Dashboard":
    st.header("🏠 Career Dashboard")
    st.info("Dashboard coming soon 🚀")

elif page == "👤 Career Profile":
    st.header("👤 My Career Profile")
    st.info("Career Profile coming soon 🚀")

elif page == "🔎 Opportunity Radar":
    st.header("🔎 Opportunity Radar")
    st.info("Opportunity Radar coming soon 🚀")

elif page == "📄 Resume & Outreach":
    st.header("📄 Resume & Outreach")
    st.info("Your existing Resume Tailor will live here.")

elif page == "🧠 Skill Gap Analyzer":
    st.header("🧠 Skill Gap Analyzer")
    st.info("Skill Gap Analyzer coming soon 🚀")

elif page == "🗺️ Career Roadmap":
    st.header("🗺️ Career Roadmap")
    st.info("Career Roadmap coming soon 🚀")

elif page == "📋 Application Tracker":
    st.header("📋 Application Tracker")
    st.info("Application Tracker coming soon 🚀")

elif page == "🎤 Interview Coach":
    st.header("🎤 Interview Coach")
    st.info("Interview Coach coming soon 🚀")

elif page == "💡 Product Builder":
    st.header("💡 Product Builder")
    st.info("Your existing Hackathon MVP Scoper will live here.")
