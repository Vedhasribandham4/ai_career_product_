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
# ROLE SKILL REQUIREMENTS
# =========================================================

ROLE_SKILLS = {

    "Software Engineer": [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Git/GitHub"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Data Analysis",
        "Data Visualization"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Data Visualization"
    ],

    "Machine Learning Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "SQL",
        "Git/GitHub"
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "SQL",
        "Git/GitHub",
        "Cloud Computing"
    ],

    "Python Developer": [
        "Python",
        "SQL",
        "Git/GitHub",
        "HTML/CSS"
    ],

    "Web Developer": [
        "HTML/CSS",
        "JavaScript",
        "React",
        "Git/GitHub",
        "SQL"
    ],

    "Cloud Engineer": [
        "Python",
        "SQL",
        "Git/GitHub",
        "Cloud Computing"
    ],

    "Cybersecurity Analyst": [
        "Python",
        "C",
        "C++",
        "SQL",
        "Cybersecurity",
        "Git/GitHub"
    ]
}


# =========================================================
# SKILL GAP ANALYZER
# =========================================================

def analyze_skill_gap(profile):

    target_role = profile["target_role"]

    required_skills = ROLE_SKILLS.get(
        target_role,
        []
    )

    user_skills = set(profile["skills"])

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in user_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


# =========================================================
# CAREER READINESS SCORE
# =========================================================

def calculate_readiness(profile):

    score = 0

    # -----------------------------------------------------
    # ROLE SKILL MATCH
    # -----------------------------------------------------

    matched_skills, missing_skills = analyze_skill_gap(profile)

    required_skills = ROLE_SKILLS.get(
        profile["target_role"],
        []
    )

    if required_skills:

        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 40

        score += skill_score

    else:

        # Fallback if target role is "Other"

        if len(profile["skills"]) >= 5:
            score += 40

        elif len(profile["skills"]) >= 3:
            score += 30

        elif len(profile["skills"]) >= 1:
            score += 20


    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    if profile["projects"].strip():
        score += 20


    # -----------------------------------------------------
    # EXPERIENCE
    # -----------------------------------------------------

    if profile["experience"].strip():
        score += 20


    # -----------------------------------------------------
    # EDUCATION
    # -----------------------------------------------------

    if profile["cgpa"] >= 8:
        score += 20

    elif profile["cgpa"] >= 7:
        score += 15

    elif profile["cgpa"] >= 6:
        score += 10


    # -----------------------------------------------------
    # LIMIT SCORE TO 100
    # -----------------------------------------------------

    return min(round(score), 100)


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

        readiness_score = calculate_readiness(profile)

        matched_skills, missing_skills = analyze_skill_gap(
            profile
        )


        # -------------------------------------------------
        # WELCOME
        # -------------------------------------------------

        st.subheader(
            f"Welcome, {profile['name']} 👋"
        )

        st.write(
            "Here's a quick look at your CareerPilot profile."
        )

        st.divider()


        # -------------------------------------------------
        # CAREER READINESS
        # -------------------------------------------------

        st.subheader("🎯 Career Readiness")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Readiness Score",
                f"{readiness_score}/100"
            )

        with col2:

            if readiness_score >= 80:

                st.success(
                    "🔥 You're looking strong for your target role!"
                )

            elif readiness_score >= 60:

                st.warning(
                    "🟡 You're on the right track, "
                    "but there are areas to improve."
                )

            else:

                st.error(
                    "🔴 You have some important gaps to work on."
                )


        st.divider()


        # -------------------------------------------------
        # EDUCATION
        # -------------------------------------------------

        st.subheader("🎓 Education")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Degree",
                profile["degree"]
            )

        with col2:

            st.metric(
                "Year",
                profile["year"]
            )

        with col3:

            st.metric(
                "CGPA",
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
                f"**Target Role:** "
                f"{profile['target_role']}"
            )

        with col2:

            st.write(
                f"**Preferred Location:** "
                f"{profile['preferred_location']}"
            )


        st.divider()


        # -------------------------------------------------
        # SKILL SUMMARY
        # -------------------------------------------------

        st.subheader("💻 Skill Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.write("🟢 **Matched Skills**")

            if matched_skills:

                for skill in matched_skills:

                    st.write(f"✓ {skill}")

            else:

                st.write("No matching skills yet.")


        with col2:

            st.write("🔴 **Skill Gaps**")

            if missing_skills:

                for skill in missing_skills:

                    st.write(f"✗ {skill}")

            else:

                st.write("No major skill gaps 🎉")


        st.divider()


        # -------------------------------------------------
        # PROJECTS
        # -------------------------------------------------

        st.subheader("🚀 Projects")

        if profile["projects"]:

            st.write(
                profile["projects"]
            )

        else:

            st.write(
                "No projects added yet."
            )


        st.divider()


        # -------------------------------------------------
        # EXPERIENCE
        # -----------------------------------------------------

        st.subheader("💼 Experience")

        if profile["experience"]:

            st.write(
                profile["experience"]
            )

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

    st.write(
        "See how your current skills compare with "
        "the skills required for your target career."
    )


    if not st.session_state.career_profile:

        st.warning(
            "Please complete your Career Profile first."
        )

    else:

        profile = st.session_state.career_profile

        matched_skills, missing_skills = analyze_skill_gap(
            profile
        )


        # -------------------------------------------------
        # TARGET ROLE
        # -------------------------------------------------

        st.subheader(
            f"🎯 Target Role: {profile['target_role']}"
        )


        # -------------------------------------------------
        # SKILL MATCH SCORE
        # -------------------------------------------------

        required_skills = ROLE_SKILLS.get(
            profile["target_role"],
            []
        )

        if required_skills:

            skill_percentage = round(
                len(matched_skills)
                / len(required_skills)
                * 100
            )

            st.metric(
                "Skill Match",
                f"{skill_percentage}%"
            )


        st.divider()


        # -------------------------------------------------
        # MATCHED SKILLS
        # -------------------------------------------------

        st.subheader("🟢 Skills You Have")

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No matching skills found yet."
            )


        # -------------------------------------------------
        # MISSING SKILLS
        # -------------------------------------------------

        st.subheader("🔴 Skill Gaps")

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "🔥 You have all the core skills "
                "defined for this role!"
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

