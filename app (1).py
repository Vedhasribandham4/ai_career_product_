import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# APP HEADER
# =========================================================

st.title("🤖 CareerPilot AI")
st.caption("Your AI Career Copilot")


# =========================================================
# SESSION STATE
# =========================================================

if "career_profile" not in st.session_state:
    st.session_state.career_profile = {}


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🤖 CareerPilot AI")

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


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.header("🏠 Career Dashboard")

    if not st.session_state.career_profile:

        st.info(
            "Your career profile is empty. "
            "Go to 👤 Career Profile and add your details."
        )

    else:

        profile = st.session_state.career_profile

        st.subheader(
            f"Welcome, {profile['name']} 👋"
        )

        st.write(
            "Here's a quick look at your CareerPilot profile."
        )

        st.divider()

        # -------------------------------------------------
        # EDUCATION METRICS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🎓 Degree",
                profile["degree"]
            )

        with col2:
            st.metric(
                "📚 Year",
                profile["year"]
            )

        with col3:
            st.metric(
                "📊 CGPA",
                profile["cgpa"]
            )

        st.divider()

        # -------------------------------------------------
        # CAREER GOAL
        # -------------------------------------------------

        st.subheader("🎯 Career Goal")

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Target Role:** {profile['target_role']}"
            )

        with col2:
            st.write(
                f"**Preferred Location:** "
                f"{profile['preferred_location']}"
            )

        st.divider()

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        st.subheader("💻 Skills")

        if profile["skills"]:

            st.write(
                " • ".join(profile["skills"])
            )

        else:

            st.write(
                "No skills added yet."
            )

        st.divider()

        # -------------------------------------------------
        # PROJECTS
        # -------------------------------------------------

        st.subheader("🚀 Projects")

        if profile["projects"]:

            st.write(profile["projects"])

        else:

            st.write(
                "No projects added yet."
            )

        st.divider()

        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        st.subheader("💼 Experience")

        if profile["experience"]:

            st.write(profile["experience"])

        else:

            st.write(
                "No experience added yet."
            )


# =========================================================
# CAREER PROFILE
# =========================================================

elif page == "👤 Career Profile":

    st.header("👤 My Career Profile")

    st.write(
        "Tell CareerPilot about yourself so it can "
        "personalize your career recommendations."
    )

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    st.subheader("👤 Basic Information")

    name = st.text_input(
        "Your Name"
    )

    col1, col2 = st.columns(2)

    with col1:

        degree = st.selectbox(
            "Degree",
            [
                "B.Tech",
                "B.E.",
                "B.Sc",
                "BCA",
                "MCA",
                "M.Tech",
                "Other"
            ]
        )

    with col2:

        year = st.selectbox(
            "Current Year",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year",
                "Graduate"
            ]
        )

    branch = st.text_input(
        "Branch / Specialization",
        placeholder="e.g. Computer Science, Data Science"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        step=0.01
    )

    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    st.subheader("💻 Skills")

    skills = st.multiselect(
        "Select your skills",
        [
            "Python",
            "Java",
            "C",
            "C++",
            "SQL",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "Data Analysis",
            "Data Visualization",
            "HTML/CSS",
            "JavaScript",
            "React",
            "Git/GitHub",
            "Cloud Computing",
            "Cybersecurity"
        ]
    )

    # -----------------------------------------------------
    # CAREER GOAL
    # -----------------------------------------------------

    st.subheader("🎯 Career Goal")

    target_role = st.selectbox(
        "Target Career Role",
        [
            "Software Engineer",
            "Data Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Python Developer",
            "Web Developer",
            "Cloud Engineer",
            "Cybersecurity Analyst",
            "Other"
        ]
    )

    preferred_location = st.text_input(
        "📍 Preferred Location",
        placeholder="e.g. Hyderabad, Bengaluru, Remote"
    )

    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    st.subheader("🚀 Projects")

    projects = st.text_area(
        "Tell us about your projects",
        placeholder=(
            "Example: AI Resume Analyzer using "
            "Python, Streamlit and Groq API"
        ),
        height=120
    )

    # -----------------------------------------------------
    # EXPERIENCE
    # -----------------------------------------------------

    st.subheader("💼 Internships / Experience")

    experience = st.text_area(
        "Tell us about your experience",
        placeholder=(
            "Mention internships, freelance work, "
            "volunteering, or relevant experience."
        ),
        height=100
    )

    # -----------------------------------------------------
    # SAVE PROFILE
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "💾 Save Career Profile",
        type="primary"
    ):

        st.session_state.career_profile = {

            "name": name,

            "degree": degree,

            "year": year,

            "branch": branch,

            "cgpa": cgpa,

            "skills": skills,

            "target_role": target_role,

            "preferred_location": preferred_location,

            "projects": projects,

            "experience": experience
        }

        st.success(
            "Career profile saved successfully! 🎉"
        )


# =========================================================
# OPPORTUNITY RADAR
# =========================================================

elif page == "🔎 Opportunity Radar":

    st.header("🔎 Opportunity Radar")

    st.info(
        "AI-powered internship and job recommendations "
        "will appear here 🚀"
    )


# =========================================================
# RESUME & OUTREACH
# =========================================================

elif page == "📄 Resume & Outreach":

    st.header("📄 Resume & Outreach")

    st.info(
        "Your existing Resume Tailor will live here."
    )


# =========================================================
# SKILL GAP ANALYZER
# =========================================================

elif page == "🧠 Skill Gap Analyzer":

    st.header("🧠 Skill Gap Analyzer")

    st.info(
        "AI skill gap analysis will appear here 🧠"
    )


# =========================================================
# CAREER ROADMAP
# =========================================================

elif page == "🗺️ Career Roadmap":

    st.header("🗺️ Career Roadmap")

    st.info(
        "Your personalized career roadmap will appear here 🗺️"
    )


# =========================================================
# APPLICATION TRACKER
# =========================================================

elif page == "📋 Application Tracker":

    st.header("📋 Application Tracker")

    st.info(
        "Your internship and job applications "
        "will appear here 📋"
    )


# =========================================================
# INTERVIEW COACH
# =========================================================

elif page == "🎤 Interview Coach":

    st.header("🎤 Interview Coach")

    st.info(
        "AI interview preparation will appear here 🎤"
    )


# =========================================================
# PRODUCT BUILDER
# =========================================================

elif page == "💡 Product Builder":

    st.header("💡 Product Builder")

    st.info(
        "Your existing Hackathon MVP Scoper "
        "will live here 💡"
    )

