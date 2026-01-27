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

# ---------------- Roadmap Logic ----------------
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

# ---------------- ADDITIONAL FEATURE ----------------
# -------- Job-based Skill Analysis Data --------
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
st.caption("Main roadmap system with additional Skill Analysis option")
st.divider()

# ---------------- Inputs ----------------
st.header("📋 Student Details")

name = st.text_input("Student Name")
year = st.selectbox("Year", [1, 2, 3, 4])
branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE"])
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Study Hours / Day", 0, 12, 3)
hostel = st.selectbox("Hostel", ["Yes", "No"])
stress = st.selectbox("Stress Level", ["Low", "Medium", "High"])
confusion = st.selectbox("Confusion Level", ["Low", "Medium", "High"])
communication = st.selectbox("Communication Skill", ["Poor", "Average", "Good"])
budget = st.selectbox("Budget", ["Low", "Medium", "High"])
interest = st.selectbox("Primary Interest", ["Programming", "Web", "Data Science"])

st.divider()

# ---------------- Generate Roadmap ----------------
if st.button("🔍 Generate My Roadmap"):
    student_info = {
        "skill_level": "Beginner",
        "study_hours": study_hours,
        "gpa": gpa,
        "stress_level": stress,
        "communication": communication,
        "budget": budget,
        "interest": interest
    }

    roadmap = generate_roadmap(student_info)

    st.success(f"Roadmap generated for {name or 'Student'}")

    for i, step in enumerate(roadmap, 1):
        st.write(f"{i}. {step}")

st.divider()

# =================================================================
# 🔹 ADDITIONAL OPTIONAL FEATURE: SKILL ANALYSIS
# =================================================================

st.header("🧩 Skill Analysis (Optional)")
st.caption("Explore job roles and identify what you need to learn")

job_choice = st.selectbox(
    "Choose a job role to explore",
    list(JOB_SKILL_ANALYSIS.keys())
)

job_info = JOB_SKILL_ANALYSIS[job_choice]

# Show skills, projects, resources side-by-side
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

# Ask user skills
st.divider()
st.subheader("🎓 Your Current Skills")

known_skills = st.multiselect(
    "Select skills you already know",
    job_info["skills"]
)

# Skill gap analysis
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
    for s in missing:
        st.error(s)

# Learning order
st.subheader("🛣️ Recommended Learning Order")
for i, skill in enumerate(missing, 1):
    st.write(f"{i}. Learn **{skill}**")

st.divider()

with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("Mini Project | Personalized Student Skill Roadmap + Skill Analysis Module")
