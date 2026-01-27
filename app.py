import streamlit as st
import pandas as pd
from datetime import date

# ---------------- Page Config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    return pd.read_csv("student_performance_extended.csv")

data = load_data()

# ---------------- Helpers ----------------
def safe_unique(df, col, fallback):
    return sorted(df[col].dropna().unique()) if col in df.columns else fallback

def normalize_yes_no(x):
    if isinstance(x, str):
        x = x.strip().lower()
        if x in ("yes", "y", "true", "1"):
            return "Yes"
    return "No"

# ---------------- Roadmap Logic ----------------
def build_week_plan(interest, skill_level, budget_level):
    free_note = "Use free resources (YouTube/NPTEL/free Coursera audits)." if budget_level == "Low" else "Consider 1 paid course + mentorship for speed."
    if skill_level == "Beginner":
        project = "Mini project: build a basic end-to-end demo"
        depth = "Focus on fundamentals + consistent practice"
    else:
        project = "Project: build a portfolio-grade real-world application"
        depth = "Focus on advanced concepts + real datasets + deployment"
    return [
        {
            "title": "Week 1 — Foundation",
            "bullets": [
                f"{depth} in **{interest}** (core concepts).",
                "Set up tools (GitHub, editor, notes).",
                "Daily practice: 45–60 mins.",
                free_note,
            ],
        },
        {
            "title": "Week 2 — Skill Building",
            "bullets": [
                "Solve 10–15 practice problems / exercises.",
                "Start a structured course + take notes.",
                "Build 1 small component (feature/module) daily.",
            ],
        },
        {
            "title": "Week 3 — Projects & Proof",
            "bullets": [
                project,
                "Add README + screenshots + clear steps.",
                "Push code daily to GitHub (commit streak).",
            ],
        },
        {
            "title": "Week 4 — Career Readiness",
            "bullets": [
                "Resume: add project + skills + links.",
                "Mock interview / presentations (2 sessions).",
                "Polish project + deploy (if possible).",
                "Plan next month based on gaps.",
            ],
        },
    ]

def generate_roadmap(info):
    steps = []

    if info['skill_level'] == "Beginner":
        steps.append("Start with basics and practice small projects.")
    else:
        steps.append("Focus on advanced projects and real-world applications.")

    if info['study_hours'] < 3 or info['gpa'] < 6.0:
        steps.append("Increase study hours and follow a structured schedule.")

    if info['stress_level'] == "High":
        steps.append("Adopt stress management techniques and time planning.")

    if info['communication'] == "Poor":
        steps.append("Improve communication via speaking and writing practice.")

    if info['budget'] == "Low":
        steps.append("Use free learning platforms and open resources.")
    else:
        steps.append("Consider paid courses for faster progress.")

    steps.append(f"Focus learning on your interest: {info['interest']}.")

    return steps

# ---------------- Skill Gap Analysis ----------------
JOB_SKILL_ANALYSIS = {
    "Software Developer": {
        "skills": [
            "Python / Java",
            "Data Structures & Algorithms",
            "HTML, CSS, JavaScript",
            "Git & GitHub",
            "Databases (SQL)",
            "OOPS",
            "Problem Solving"
        ],
        "projects": [
            "Student Management System",
            "Task Tracker Application",
            "Portfolio Website",
            "REST API Mini Project"
        ],
        "resources": [
            "NPTEL – Programming & DSA",
            "YouTube – freeCodeCamp",
            "GeeksForGeeks – DSA",
            "GitHub – Open Source Projects"
        ]
    },
    "Frontend Developer": {
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Responsive Design",
            "Git & GitHub"
        ],
        "projects": [
            "Portfolio Website",
            "React To-Do App",
            "UI Clone (Netflix / Amazon)"
        ],
        "resources": [
            "MDN Web Docs",
            "Traversy Media (YouTube)",
            "React Official Docs"
        ]
    },
    "Data Scientist": {
        "skills": [
            "Python",
            "Statistics",
            "Pandas & NumPy",
            "Data Visualization",
            "Machine Learning Basics"
        ],
        "projects": [
            "Student Performance Analysis",
            "Sales Prediction Model",
            "EDA Project"
        ],
        "resources": [
            "Kaggle Learn",
            "Krish Naik (YouTube)",
            "Coursera ML (Audit Mode)"
        ]
    }
}

def compute_skill_gap(required_skills, known_skills):
    known = []
    missing = []
    for s in required_skills:
        if s in known_skills:
            known.append(s)
        else:
            missing.append(s)
    return known, missing

# ---------------- UI ----------------
st.title("🎓 Personalized Student Skill Roadmap")
st.caption("Student roadmap with week-wise plan and optional Skill Analysis")
st.divider()

# ---------------- Inputs ----------------
st.header("📋 Student Details")

name = st.text_input("Student Name")
year = st.selectbox("Year", [1, 2, 3, 4])
branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE"])
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Daily Study Hours", 0, 12, 3)
failures = st.number_input("Number of Failures", min_value=0, max_value=10, value=0)
hostel = st.selectbox("Hostel?", ["Yes", "No"])
sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 6)
family_support = st.selectbox("Family Support Level", ["Low", "Medium", "High"])
interest = st.selectbox("Primary Interest", ["Programming", "Web", "Data Science"])
budget = st.selectbox("Budget Level", ["Low", "Medium", "High"])
skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
confusion_level = st.selectbox("Confusion Level", ["Low", "Medium", "High"])
communication = st.selectbox("Communication Level", ["Poor", "Average", "Good"])

st.divider()

# ---------------- Generate Roadmap ----------------
if st.button("🔍 Generate My Roadmap"):
    student_info = {
        "year": year,
        "branch": branch,
        "gpa": float(gpa),
        "study_hours": int(study_hours),
        "failures": int(failures),
        "hostel": hostel,
        "sleep_hours": int(sleep_hours),
        "family_support": family_support,
        "interest": interest,
        "budget": budget,
        "skill_level": skill_level,
        "stress_level": stress_level,
        "confusion_level": confusion_level,
        "communication": communication,
    }

    roadmap = generate_roadmap(student_info)

    st.success(f"✅ Roadmap Generated for {name or 'Student'}")

    # Quick dashboard metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", f"{gpa:.1f}")
    col2.metric("Study Hours/day", f"{study_hours}")
    col3.metric("Sleep Hours", f"{sleep_hours}")

    # Simple readiness score
    readiness = 0
    readiness += 30 if gpa >= 7 else 20 if gpa >= 6 else 10
    readiness += 25 if study_hours >= 4 else 15 if study_hours >= 3 else 8
    readiness += 20 if stress_level != "High" else 8
    readiness += 15 if confusion_level != "High" else 8
    readiness += 10 if communication in ("Average", "Good") else 5
    readiness = min(readiness, 100)
    st.write("### 📈 Readiness Score")
    st.progress(readiness / 100)
    st.caption("UI indicator only, not an official assessment")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🧭 Roadmap", "🗓️ 4-Week Plan", "🧪 Projects", "📚 Resources"])

    with tab1:
        st.subheader("✅ Action Steps")
        for i, step in enumerate(roadmap, 1):
            st.write(f"{i}. {step}")

    with tab2:
        week_plan = build_week_plan(interest, skill_level, budget)
        for w in week_plan:
            with st.expander(w["title"], expanded=True):
                for b in w["bullets"]:
                    st.write(f"• {b}")

    with tab3:
        st.subheader("Suggested Projects")
        project_list = ["Sample project 1", "Sample project 2"]  # placeholder
        for p in project_list:
            st.write(f"🚀 {p}")

    with tab4:
        st.subheader("Recommended Resources")
        resource_list = ["Sample resource 1", "Sample resource 2"]  # placeholder
        for r in resource_list:
            st.write(f"📌 {r}")

st.divider()

# =================================================================
# 🔹 OPTIONAL FEATURE: SKILL GAP ANALYSIS
# =================================================================
st.header("🧩 Skill Analysis (Optional)")
st.caption("Select a job role and see the skills, projects, resources and gaps")

job_choice = st.selectbox(
    "Choose a job role to explore",
    ["-- Select Job Role --"] + list(JOB_SKILL_ANALYSIS.keys())
)

if job_choice != "-- Select Job Role --":
    job_info = JOB_SKILL_ANALYSIS[job_choice]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🧠 Skills Required")
        for s in job_info["skills"]:
            st.write("•", s)
    with col2:
        st.subheader("🧪 Projects")
        for p in job_info["projects"]:
            st.write("•", p)
    with col3:
        st.subheader("📚 Resources")
        for r in job_info["resources"]:
            st.write("•", r)

    st.divider()
    st.subheader("🎓 Your Current Skills")
    known_skills = st.multiselect("Select skills you already know", job_info["skills"])

    known, missing = compute_skill_gap(job_info["skills"], known_skills)

    st.subheader("📊 Skill Gap Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Skills You Have")
        if known:
            for s in known:
                st.success(s)
        else:
            st.warning("No skills selected")
    with col2:
        st.markdown("### ❌ Skills You Need to Learn")
        if missing:
            for s in missing:
                st.error(s)
        else:
            st.success("You already know all required skills 🎉")

    if missing:
        st.subheader("🛣️ Recommended Learning Order")
        for i, skill in enumerate(missing, 1):
            st.write(f"{i}. Learn **{skill}**")
else:
    st.info("👆 Please select a job role to see skills, projects, and skill gap analysis.")

st.divider()
with st.expander("📊 Sample Student Dataset"):
    st.dataframe(data)

st.caption("Mini Project | Personalized Student Skill Roadmap + Skill Gap Analysis")
