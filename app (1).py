import os
import json

import streamlit as st
from groq import Groq
from pypdf import PdfReader
from docx import Document


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 CareerPilot AI")
st.caption("Your AI Career Copilot")


# =========================================================
# SESSION STATE
# =========================================================

if "career_profile" not in st.session_state:
    st.session_state.career_profile = {}

if "applications" not in st.session_state:
    st.session_state.applications = []

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


# =========================================================
# GROQ API
# =========================================================

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None


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
# DEMO OPPORTUNITIES
# =========================================================

OPPORTUNITIES = [

    {
        "id": 1,
        "title": "Data Analyst Intern",
        "company": "TechNova",
        "location": "Hyderabad",
        "type": "Internship",
        "required_skills": [
            "Python",
            "SQL",
            "Pandas",
            "Data Visualization"
        ],
        "description": (
            "Work with datasets, dashboards and "
            "business analytics."
        )
    },

    {
        "id": 2,
        "title": "Python Developer Intern",
        "company": "CodeWorks",
        "location": "Hyderabad",
        "type": "Internship",
        "required_skills": [
            "Python",
            "SQL",
            "Git/GitHub"
        ],
        "description": (
            "Build backend applications using Python."
        )
    },

    {
        "id": 3,
        "title": "Machine Learning Intern",
        "company": "AI Labs",
        "location": "Bengaluru",
        "type": "Internship",
        "required_skills": [
            "Python",
            "NumPy",
            "Pandas",
            "Machine Learning"
        ],
        "description": (
            "Develop machine learning models "
            "and experiments."
        )
    },

    {
        "id": 4,
        "title": "Frontend Developer Intern",
        "company": "WebCraft",
        "location": "Remote",
        "type": "Internship",
        "required_skills": [
            "HTML/CSS",
            "JavaScript",
            "React",
            "Git/GitHub"
        ],
        "description": (
            "Build modern web interfaces "
            "and frontend applications."
        )
    },

    {
        "id": 5,
        "title": "Cybersecurity Intern",
        "company": "SecureNet",
        "location": "Hyderabad",
        "type": "Internship",
        "required_skills": [
            "Python",
            "Cybersecurity",
            "SQL",
            "Git/GitHub"
        ],
        "description": (
            "Assist with security monitoring "
            "and vulnerability analysis."
        )
    }
]


# =========================================================
# RESUME FILE EXTRACTION
# =========================================================

def extract_resume_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    # -----------------------------
    # PDF
    # -----------------------------

    if file_name.endswith(".pdf"):

        try:
            pdf = PdfReader(uploaded_file)

            pages_text = []

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    pages_text.append(page_text)

            return "\n".join(pages_text).strip()

        except Exception as e:

            st.error(
                f"Could not read PDF: {e}"
            )

            return ""

    # -----------------------------
    # DOCX
    # -----------------------------

    if file_name.endswith(".docx"):

        try:

            document = Document(uploaded_file)

            paragraphs = []

            for paragraph in document.paragraphs:

                text = paragraph.text.strip()

                if text:
                    paragraphs.append(text)

            return "\n".join(paragraphs).strip()

        except Exception as e:

            st.error(
                f"Could not read DOCX: {e}"
            )

            return ""

    return ""


# =========================================================
# SKILL GAP ANALYZER
# =========================================================

def analyze_skill_gap(profile):

    target_role = profile.get(
        "target_role",
        "Other"
    )

    required_skills = ROLE_SKILLS.get(
        target_role,
        []
    )

    user_skills = set(
        profile.get("skills", [])
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in user_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


# =========================================================
# OPPORTUNITY MATCHING
# =========================================================

def calculate_opportunity_match(
    profile,
    opportunity
):

    user_skills = set(
        profile.get("skills", [])
    )

    required_skills = set(
        opportunity.get(
            "required_skills",
            []
        )
    )

    matched_skills = user_skills.intersection(
        required_skills
    )

    missing_skills = required_skills.difference(
        user_skills
    )

    if required_skills:

        match_percentage = round(
            len(matched_skills)
            / len(required_skills)
            * 100
        )

    else:

        match_percentage = 0

    return (
        match_percentage,
        sorted(matched_skills),
        sorted(missing_skills)
    )


# =========================================================
# CAREER READINESS
# =========================================================

def calculate_readiness(profile):

    score = 0

    matched_skills, _ = analyze_skill_gap(
        profile
    )

    required_skills = ROLE_SKILLS.get(
        profile.get("target_role", "Other"),
        []
    )

    # -----------------------------
    # Skills - 40 points
    # -----------------------------

    if required_skills:

        score += (
            len(matched_skills)
            / len(required_skills)
        ) * 40

    else:

        skill_count = len(
            profile.get("skills", [])
        )

        if skill_count >= 5:
            score += 40

        elif skill_count >= 3:
            score += 30

        elif skill_count >= 1:
            score += 20

    # -----------------------------
    # Projects - 20 points
    # -----------------------------

    if profile.get(
        "projects",
        ""
    ).strip():

        score += 20

    # -----------------------------
    # Experience - 20 points
    # -----------------------------

    if profile.get(
        "experience",
        ""
    ).strip():

        score += 20

    # -----------------------------
    # CGPA - 20 points
    # -----------------------------

    cgpa = profile.get(
        "cgpa",
        0
    )

    if cgpa >= 8:
        score += 20

    elif cgpa >= 7:
        score += 15

    elif cgpa >= 6:
        score += 10

    return min(
        round(score),
        100
    )


# =========================================================
# GENERIC GROQ REQUEST
# =========================================================

def ask_groq(
    prompt,
    temperature=0.3,
    json_mode=False
):

    if client is None:

        return None

    try:

        request = {

            "model": "llama-3.3-70b-versatile",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "temperature": temperature
        }

        if json_mode:

            request["response_format"] = {
                "type": "json_object"
            }

        response = client.chat.completions.create(
            **request
        )

        return response.choices[
            0
        ].message.content

    except Exception as e:

        st.error(
            f"AI request failed: {e}"
        )

        return None


# =========================================================
# AI OPPORTUNITY ANALYSIS
# =========================================================

def generate_opportunity_analysis(
    profile,
    opportunity,
    matched_skills,
    missing_skills
):

    prompt = f"""
You are CareerPilot AI, an AI career advisor.

Help a college student decide whether they should
apply for an internship.

STUDENT PROFILE

Target Role:
{profile.get("target_role", "Not provided")}

Skills:
{", ".join(profile.get("skills", []))}

Projects:
{profile.get("projects", "None")}

Experience:
{profile.get("experience", "None")}


OPPORTUNITY

Title:
{opportunity["title"]}

Company:
{opportunity["company"]}

Location:
{opportunity["location"]}

Required Skills:
{", ".join(opportunity["required_skills"])}

Skills Student Has:
{", ".join(matched_skills)}

Missing Skills:
{", ".join(missing_skills)}


Return exactly these sections:

### WHY APPLY

Explain why the student is reasonably suited.

### SKILL GAP

Explain the most important missing skills.

### ACTION PLAN

Give 3 practical steps the student can take
before or while applying.

### FINAL ADVICE

Clearly choose ONE:

APPLY NOW

APPLY AFTER PREPARATION

BUILD MORE SKILLS FIRST

Never invent skills, achievements,
experience, certifications or projects.
"""

    result = ask_groq(
        prompt,
        temperature=0.3
    )

    if result is None:

        return (
            "Unable to generate AI analysis. "
            "Please check your Groq API configuration."
        )

    return result


# =========================================================
# AI RESUME / OUTREACH
# =========================================================

def generate_outreach(
    resume,
    job_description,
    output_type
):

    prompts = {

        "LinkedIn Summary": f"""
Write a professional LinkedIn About summary.

Only use facts from the resume.
Do not invent information.

Maximum 3 short paragraphs.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
""",

        "LinkedIn DM": f"""
Write a professional LinkedIn message
to a recruiter.

Maximum 75 words.

Use only facts from the resume.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
""",

        "Cold Email": f"""
Write a professional cold email
to a hiring manager.

Include:

- Subject line
- Short introduction
- Relevant skills
- Clear call to action

Only use facts from the resume.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
""",

        "Cover Letter": f"""
Write a professional cover letter.

Structure:

- Greeting
- Opening
- Relevant skills or experience
- Why the candidate fits
- Closing

Only use facts from the resume.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
"""
    }

    prompt = prompts.get(
        output_type
    )

    if not prompt:
        return None

    return ask_groq(
        prompt,
        temperature=0.3
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🤖 CareerPilot AI")

if client is None:

    st.sidebar.warning(
        "⚠️ Groq API not configured"
    )

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

        st.stop()

    profile = st.session_state.career_profile

    readiness_score = calculate_readiness(
        profile
    )

    matched_skills, missing_skills = analyze_skill_gap(
        profile
    )

    st.subheader(
        f"Welcome, {profile.get('name', 'Student')} 👋"
    )

    st.write(
        "Here's your personalized CareerPilot overview."
    )

    st.divider()

    # -----------------------------
    # Readiness
    # -----------------------------

    st.subheader("🎯 Career Readiness")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Readiness Score",
            f"{readiness_score}/100"
        )

        st.progress(
            readiness_score / 100
        )

    with col2:

        if readiness_score >= 80:

            st.success(
                "🔥 Excellent! You're looking strong."
            )

        elif readiness_score >= 60:

            st.warning(
                "🟡 Good progress. A few gaps remain."
            )

        else:

            st.error(
                "🔴 Focus on building your skills."
            )

    st.divider()

    # -----------------------------
    # Education
    # -----------------------------

    st.subheader("🎓 Education")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Degree",
            profile.get("degree", "-")
        )

    with col2:
        st.metric(
            "Year",
            profile.get("year", "-")
        )

    with col3:
        st.metric(
            "CGPA",
            profile.get("cgpa", 0)
        )

    st.divider()

    # -----------------------------
    # Career
    # -----------------------------

    st.subheader("🎯 Career Goal")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Target Role:** "
            f"{profile.get('target_role', '-')}"
        )

    with col2:

        st.write(
            f"**Preferred Location:** "
            f"{profile.get('preferred_location', '-')}"
        )

    st.divider()

    # -----------------------------
    # Skills
    # -----------------------------

    st.subheader("💻 Skill Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🟢 **Matched Skills**")

        if matched_skills:

            for skill in matched_skills:
                st.write(f"✓ {skill}")

        else:

            st.write(
                "No matching skills yet."
            )

    with col2:

        st.write("🔴 **Skill Gaps**")

        if missing_skills:

            for skill in missing_skills:
                st.write(f"✗ {skill}")

        else:

            st.write(
                "No major skill gaps 🎉"
            )

    st.divider()

    st.subheader("🚀 Projects")

    st.write(
        profile.get(
            "projects",
            "No projects added."
        )
    )

    st.divider()

    st.subheader("💼 Experience")

    st.write(
        profile.get(
            "experience",
            "No experience added."
        )
    )


# =========================================================
# CAREER PROFILE
# =========================================================

elif page == "👤 Career Profile":

    st.header("👤 My Career Profile")

    st.write(
        "Tell CareerPilot about yourself so it can "
        "personalize your recommendations."
    )

    st.subheader("👤 Basic Information")

    existing = st.session_state.career_profile

    name = st.text_input(
        "Your Name",
        value=existing.get("name", "")
    )

    col1, col2 = st.columns(2)

    with col1:

        degree_options = [
            "B.Tech",
            "B.E.",
            "B.Sc",
            "BCA",
            "MCA",
            "M.Tech",
            "Other"
        ]

        current_degree = existing.get(
            "degree",
            "B.Tech"
        )

        degree_index = (
            degree_options.index(current_degree)
            if current_degree in degree_options
            else 0
        )

        degree = st.selectbox(
            "Degree",
            degree_options,
            index=degree_index
        )

    with col2:

        year_options = [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year",
            "Graduate"
        ]

        current_year = existing.get(
            "year",
            "1st Year"
        )

        year_index = (
            year_options.index(current_year)
            if current_year in year_options
            else 0
        )

        year = st.selectbox(
            "Current Year",
            year_options,
            index=year_index
        )

    branch = st.text_input(
        "Branch / Specialization",
        value=existing.get("branch", ""),
        placeholder=(
            "e.g. Computer Science, Data Science"
        )
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=float(
            existing.get("cgpa", 0.0)
        ),
        step=0.01
    )

    st.subheader("💻 Skills")

    skill_options = [
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

    existing_skills = existing.get(
        "skills",
        []
    )

    valid_existing_skills = [
        skill
        for skill in existing_skills
        if skill in skill_options
    ]

    skills = st.multiselect(
        "Select your skills",
        skill_options,
        default=valid_existing_skills
    )

    st.subheader("🎯 Career Goal")

    role_options = [
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

    current_role = existing.get(
        "target_role",
        "Software Engineer"
    )

    role_index = (
        role_options.index(current_role)
        if current_role in role_options
        else 0
    )

    target_role = st.selectbox(
        "Target Career Role",
        role_options,
        index=role_index
    )

    preferred_location = st.text_input(
        "📍 Preferred Location",
        value=existing.get(
            "preferred_location",
            ""
        ),
        placeholder=(
            "e.g. Hyderabad, Bengaluru, Remote"
        )
    )

    st.subheader("🚀 Projects")

    projects = st.text_area(
        "Tell us about your projects",
        value=existing.get(
            "projects",
            ""
        ),
        placeholder=(
            "Example: AI Resume Analyzer using "
            "Python, Streamlit and Groq API"
        ),
        height=120
    )

    st.subheader("💼 Internships / Experience")

    experience = st.text_area(
        "Tell us about your experience",
        value=existing.get(
            "experience",
            ""
        ),
        placeholder=(
            "Mention internships, freelance work "
            "or relevant experience."
        ),
        height=100
    )

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

    st.caption(
        "Demo opportunities for testing your CareerPilot matching system."
    )

    if not st.session_state.career_profile:

        st.warning(
            "Please complete your Career Profile first."
        )

        st.stop()

    profile = st.session_state.career_profile

    col1, col2 = st.columns(2)

    with col1:

        selected_type = st.selectbox(
            "Opportunity Type",
            [
                "All",
                "Internship"
            ]
        )

    with col2:

        selected_location = st.selectbox(
            "Location",
            [
                "All",
                "Hyderabad",
                "Bengaluru",
                "Remote"
            ]
        )

    st.divider()

    opportunities = []

    for opportunity in OPPORTUNITIES:

        if (
            selected_type != "All"
            and opportunity["type"] != selected_type
        ):
            continue

        if (
            selected_location != "All"
            and opportunity["location"] != selected_location
        ):
            continue

        (
            match_percentage,
            matched_skills,
            missing_skills
        ) = calculate_opportunity_match(
            profile,
            opportunity
        )

        opportunities.append(
            (
                match_percentage,
                opportunity,
                matched_skills,
                missing_skills
            )
        )

    opportunities.sort(
        key=lambda item: item[0],
        reverse=True
    )

    st.subheader(
        "🔥 Recommended Opportunities"
    )

    if not opportunities:

        st.info(
            "No opportunities match your filters."
        )

    for (
        match_percentage,
        opportunity,
        matched_skills,
        missing_skills
    ) in opportunities:

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.subheader(
                    opportunity["title"]
                )

                st.write(
                    f"🏢 **{opportunity['company']}**"
                )

                st.write(
                    f"📍 {opportunity['location']} "
                    f"• 💼 {opportunity['type']}"
                )

                st.write(
                    opportunity["description"]
                )

            with col2:

                st.metric(
                    "🎯 Match",
                    f"{match_percentage}%"
                )

            if matched_skills:

                st.write(
                    "🟢 **Skills you have:** "
                    + ", ".join(matched_skills)
                )

            if missing_skills:

                st.write(
                    "🔴 **Missing:** "
                    + ", ".join(missing_skills)

                )

            else:

                st.success(
                    "🔥 You meet all listed requirements!"
                )

            st.divider()

            if st.button(
                "✨ Analyze My Chances",
                key=f"analyze_{opportunity['id']}"
            ):

                with st.spinner(
                    "CareerPilot is analyzing..."
                ):

                    analysis = generate_opportunity_analysis(
                        profile,
                        opportunity,
                        matched_skills,
                        missing_skills
                    )

                st.markdown(
                    "### 🤖 CareerPilot Analysis"
                )

                st.markdown(
                    analysis
                )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "📋 Add to Applications",
                    key=f"track_{opportunity['id']}"
                ):

                    application = {
                        "title": opportunity["title"],
                        "company": opportunity["company"],
                        "location": opportunity["location"],
                        "status": "Saved"
                    }

                    if application not in st.session_state.applications:

                        st.session_state.applications.append(
                            application
                        )

                        st.success(
                            "Added to Application Tracker! 🎉"
                        )

                    else:

                        st.info(
                            "Already in your applications."
                        )

            with col2:

                if st.button(
                    "🚀 Mark as Applied",
                    key=f"apply_{opportunity['id']}"
                ):

                    application = {
                        "title": opportunity["title"],
                        "company": opportunity["company"],
                        "location": opportunity["location"],
                        "status": "Applied"
                    }

                    if application not in st.session_state.applications:

                        st.session_state.applications.append(
                            application
                        )

                    st.success(
                        "Application recorded! 🚀"
                    )


# =========================================================
# RESUME & OUTREACH
# =========================================================

elif page == "📄 Resume & Outreach":

    st.header("📄 Resume & Outreach")

    st.write(
        "Upload your resume and create "
        "AI-powered career content."
    )

    st.divider()

    # -----------------------------
    # Upload
    # -----------------------------

    st.subheader("📎 Upload Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Upload a PDF or DOCX resume."
    )

    if uploaded_resume:

        if st.button(
            "📖 Extract Resume",
            type="primary"
        ):

            with st.spinner(
                "Reading your resume..."
            ):

                extracted_text = extract_resume_text(
                    uploaded_resume
                )

            if extracted_text:

                st.session_state.resume_text = (
                    extracted_text
                )

                st.success(
                    "Resume successfully extracted! 🎉"
                )

            else:

                st.error(
                    "Could not extract text from this file."
                )

    # -----------------------------
    # Resume preview
    # -----------------------------

    if st.session_state.resume_text:

        st.subheader("📄 Resume Preview")

        with st.expander(
            "View extracted resume text"
        ):

            st.text_area(
                "Extracted Resume",
                value=st.session_state.resume_text,
                height=300,
                label_visibility="collapsed"
            )

        st.success(
            "✅ Resume is ready for AI processing."
        )

    else:

        st.info(
            "Upload a PDF or DOCX resume above."
        )

    st.divider()

    # -----------------------------
    # Job description
    # -----------------------------

    st.subheader("💼 Target Opportunity")

    jd_input = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Paste the internship or job description "
            "you want to target..."
        )
    )

    # -----------------------------
    # Output type
    # -----------------------------

    output_type = st.selectbox(
        "✨ What should CareerPilot generate?",
        [
            "LinkedIn Summary",
            "LinkedIn DM",
            "Cold Email",
            "Cover Letter"
        ]
    )

    st.divider()

    # -----------------------------
    # Generate
    # -----------------------------

    if st.button(
        "🚀 Generate Tailored Content",
        type="primary"
    ):

        resume = st.session_state.resume_text

        if not resume:

            st.warning(
                "📎 Please upload and extract your resume first."
            )

        elif not jd_input.strip():

            st.warning(
                "💼 Please provide a job description."
            )

        elif client is None:

            st.error(
                "⚠️ Groq API is not configured."
            )

        else:

            with st.spinner(
                "🤖 CareerPilot is analyzing your resume..."
            ):

                result = generate_outreach(
                    resume,
                    jd_input,
                    output_type
                )

            if result:

                st.success(
                    "✨ Generated successfully!"
                )

                st.subheader(
                    f"🤖 Generated {output_type}"
                )

                st.markdown(
                    result
                )

                st.divider()

                st.download_button(
                    label="📥 Download Content",
                    data=result,
                    file_name=(
                        "careerpilot_"
                        + output_type.lower().replace(
                            " ",
                            "_"
                        )
                        + ".txt"
                    ),
                    mime="text/plain"
                )


# =========================================================
# SKILL GAP ANALYZER
# =========================================================

elif page == "🧠 Skill Gap Analyzer":

    st.header("🧠 Skill Gap Analyzer")

    if not st.session_state.career_profile:

        st.warning(
            "Please complete your Career Profile first."
        )

        st.stop()

    profile = st.session_state.career_profile

    matched_skills, missing_skills = analyze_skill_gap(
        profile
    )

    required_skills = ROLE_SKILLS.get(
        profile.get("target_role"),
        []
    )

    st.subheader(
        f"🎯 Target Role: {profile.get('target_role')}"
    )

    if required_skills:

        percentage = round(
            len(matched_skills)
            / len(required_skills)
            * 100
        )

        st.metric(
            "Skill Match",
            f"{percentage}%"
        )

        st.progress(
            percentage / 100
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🟢 Skills You Have"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No matching skills yet."
            )

    with col2:

        st.subheader(
            "🔴 Skills To Learn"
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "🔥 You have all core skills!"
            )


# =========================================================
# CAREER ROADMAP
# =========================================================

elif page == "🗺️ Career Roadmap":

    st.header("🗺️ Career Roadmap")

    if not st.session_state.career_profile:

        st.warning(
            "Complete your Career Profile first."
        )

        st.stop()

    profile = st.session_state.career_profile

    st.subheader(
        f"🚀 Roadmap to {profile.get('target_role')}"
    )

    _, missing = analyze_skill_gap(
        profile
    )

    st.write(
        "### Step 1 — Build Core Skills"
    )

    if missing:

        for skill in missing:

            st.write(
                f"📚 Learn **{skill}**"
            )

    else:

        st.success(
            "Core skills are already covered!"
        )

    st.write(
        "### Step 2 — Build Projects"
    )

    st.write(
        "🚀 Build 2–3 projects related to your target role."
    )

    st.write(
        "### Step 3 — Apply"
    )

    st.write(
        "🎯 Start applying to internships and entry-level roles."
    )

    st.write(
        "### Step 4 — Interview Preparation"
    )

    st.write(
        "🎤 Practice technical and behavioral interviews."
    )


# =========================================================
# APPLICATION TRACKER
# =========================================================

elif page == "📋 Application Tracker":

    st.header("📋 Application Tracker")

    applications = st.session_state.applications

    if not applications:

        st.info(
            "No applications yet. "
            "Find opportunities in Opportunity Radar."
        )

    else:

        st.subheader(
            f"📊 Total Applications: {len(applications)}"
        )

        status_options = [
            "Saved",
            "Applied",
            "Assessment",
            "Interview",
            "Offer",
            "Rejected"
        ]

        for index, application in enumerate(
            applications
        ):

            with st.container(border=True):

                st.subheader(
                    application["title"]
                )

                st.write(
                    f"🏢 {application['company']}"
                )

                st.write(
                    f"📍 {application['location']}"
                )

                current_status = application.get(
                    "status",
                    "Saved"
                )

                if current_status not in status_options:
                    current_status = "Saved"

                status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(
                        current_status
                    ),
                    key=f"status_{index}"
                )

                application["status"] = status


# =========================================================
# INTERVIEW COACH
# =========================================================

elif page == "🎤 Interview Coach":

    st.header("🎤 AI Interview Coach")

    if not st.session_state.career_profile:

        st.warning(
            "Complete your Career Profile first."
        )

        st.stop()

    profile = st.session_state.career_profile

    interview_role = st.text_input(
        "Interview Role",
        value=profile.get(
            "target_role",
            ""
        )
    )

    interview_question = st.text_area(
        "Paste an interview question",
        placeholder=(
            "Example: Tell me about yourself."
        )
    )

    if st.button(
        "🤖 Generate Answer",
        type="primary"
    ):

        if client is None:

            st.error(
                "Groq API is not configured."
            )

        elif not interview_question.strip():

            st.warning(
                "Enter an interview question."
            )

        else:

            prompt = f"""
You are an expert interview coach.

Student target role:
{profile.get("target_role", "")}

Student skills:
{", ".join(profile.get("skills", []))}

Student projects:
{profile.get("projects", "None")}

Student experience:
{profile.get("experience", "None")}

Interview role:
{interview_role}

Question:
{interview_question}

Create a strong but truthful answer.

Do not invent achievements or experience.

Make the answer sound natural
for a college student.
"""

            with st.spinner(
                "Preparing your answer..."
            ):

                result = ask_groq(
                    prompt,
                    temperature=0.4
                )

            if result:

                st.markdown(
                    "### 💬 Suggested Answer"
                )

                st.write(
                    result
                )


# =========================================================
# PRODUCT BUILDER
# =========================================================

elif page == "💡 Product Builder":

    st.header("💡 AI Product Builder")

    st.write(
        "Turn a project idea into a realistic "
        "24-hour hackathon MVP."
    )

    raw_idea = st.text_input(
        "Enter your project idea",
        placeholder=(
            "Example: AI-powered waste management system"
        )
    )

    tools_available = st.multiselect(
        "Available Technologies",
        [
            "Python",
            "Streamlit",
            "HTML/CSS",
            "JavaScript",
            "React",
            "Groq API",
            "Gemini API",
            "Supabase",
            "Firebase",
            "SQL"
        ],
        default=[
            "Python",
            "Streamlit",
            "Groq API"
        ]
    )

    if st.button(
        "🚀 Scope My MVP",
        type="primary"
    ):

        if not raw_idea.strip():

            st.warning(
                "Enter a project idea first."
            )

        elif client is None:

            st.error(
                "Groq API is not configured."
            )

        else:

            prompt = f"""
You are a Senior Technical Product Manager.

Create a realistic 24-hour hackathon MVP.

PROJECT IDEA:
{raw_idea}

AVAILABLE TECHNOLOGIES:
{", ".join(tools_available)}

Return valid JSON with exactly these fields:

{{
    "project_title": "string",
    "problem_statement": "string",
    "mvp_features": [
        "feature 1",
        "feature 2",
        "feature 3"
    ],
    "tech_stack_mapping": "string"
}}

Keep the scope realistic for a student hackathon.
"""

            with st.spinner(
                "Building your MVP plan..."
            ):

                result = ask_groq(
                    prompt,
                    temperature=0.4,
                    json_mode=True
                )

            if result:

                try:

                    data = json.loads(
                        result
                    )

                    st.subheader(
                        f"📌 {data.get('project_title', 'MVP Plan')}"
                    )

                    st.write(
                        "**Problem:**",
                        data.get(
                            "problem_statement",
                            "Not provided."
                        )
                    )

                    st.write(
                        "### 🚀 MVP Features"
                    )

                    features = data.get(
                        "mvp_features",
                        []
                    )

                    if features:

                        for feature in features:

                            st.write(
                                f"• {feature}"
                            )

                    else:

                        st.write(
                            "No features returned."
                        )

                    st.info(
                        data.get(
                            "tech_stack_mapping",
                            "No tech stack mapping returned."
                        )
                    )

                except json.JSONDecodeError:

                    st.error(
                        "The AI returned an invalid JSON response."
                    )

                    st.code(
                        result,
                        language="text"
                    )


# =========================================================
# END
# =========================================================


