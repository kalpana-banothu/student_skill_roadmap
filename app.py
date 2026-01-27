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

# ---------------- Skill Maps ----------------
SKILL_MAP = {
    "Software Developer": {
        "Programming Languages": ["Python", "Java", "C++"],
        "Data Structures & Algorithms": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs"],
        "Web Basics": ["HTML", "CSS", "JavaScript"],
        "Backend Development": ["APIs", "Databases (SQL)", "Authentication"],
        "Tools": ["Git", "GitHub", "VS Code"],
        "CS Fundamentals": ["OOPS", "DBMS", "OS Basics", "Computer Networks"],
        "Career Skills": ["Problem Solving", "Debugging", "Communication"]
    },

    "Data Science": {
        "Programming": ["Python"],
        "Math": ["Statistics", "Probability", "Linear Algebra"],
        "Data Analysis": ["Pandas", "NumPy", "EDA"],
        "Visualization": ["Matplotlib", "Seaborn"],
        "Machine Learning": ["Regression", "Classification", "Clustering"],
        "Tools": ["Jupyter", "Git", "Kaggle"]
    },

    "Web Developer": {
        "Frontend": ["HTML", "CSS", "JavaScript"],
        "Frameworks": ["React"],
        "Backend": ["Node.js", "Django", "Flask"],
        "Database": ["MySQL", "MongoDB"],
        "Deployment": ["GitHub", "Netlify", "Vercel"]
    }
}

# ---------------- Skill Gap Logic ----------------
def skill_gap_analysis(interest, known_skills):
    required = SKILL_MAP.get(interest, {})
    completed, gaps = {}, {}

    for category, skills in required.items():
        done, missing = [], []
        for s in skills:
            if any(s.lower() in k.lower() for k in known_skills):
                done.append(s)
            else:
                missing.append(s)
        if done:
            completed[category] = done
        if missing:
            gaps[category] = missing

    return completed, gaps

# ---------------- Roadmap Helpers ----------------
def build_week_plan(interest):
    return [
        {
            "title": "Week 1 – Fundamentals",
            "points": [
                f"Understand core basics of {interest}",
                "Set up tools & environment",
                "Study 1–2 hours daily"
            ]
        },
        {
            "title": "Week 2 – Skill Practice",
            "points": [
                "Practice coding / exercises",
                "Start a mini project",
                "Learn Git & GitHub"
            ]
        },
        {
            "title": "Week 3 – Projects",
            "points": [
                "Complete 1 meaningful project",
                "Improve code quality",
                "Document work on GitHub"
            ]
        },
        {
            "title": "Week 4 – Career Prep",
            "points": [
                "Resume update",
                "Mock interviews",
                "Plan next learning goals"
            ]
        }
    ]

# ---------------- UI ----------------
st.title("🎓 Personalized Student Skill Roadmap")
st.caption("Career-focused learning with Skill Gap Analysis")
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

interest = st.selectbox(
    "Career Interest",
    list(SKILL_MAP.keys())
)

st.subheader("🛠️ Skills You Already Know")
known_skills = st.multiselect(
    "Select your current skills",
    [
        "Python", "Java", "C++", "HTML", "CSS", "JavaScript",
        "Git", "GitHub", "SQL", "APIs", "OOPS",
        "DBMS", "OS Basics", "Problem Solving", "Communication"
    ]
)

st.divider()

# ---------------- Generate Output ----------------
if st.button("🔍 Generate My Roadmap"):
    completed, gaps = skill_gap_analysis(interest, known_skills)
    week_plan = build_week_plan(interest)

    st.success(f"Roadmap generated for {name or 'Student'}")

    # Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", gpa)
    col2.metric("Study Hours", study_hours)
    col3.metric("Stress", stress)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Skill Gap", "🧭 Roadmap", "🗓️ 4-Week Plan", "🧪 Projects"]
    )

    # -------- Skill Gap --------
    with tab1:
        st.subheader("✅ Skills You Have")
        if completed:
            for cat, skills in completed.items():
                st.write(f"**{cat}**")
                for s in skills:
                    st.write(f"🟢 {s}")
        else:
            st.warning("No matching skills yet.")

        st.markdown("---")

        st.subheader("❌ Skills You Need to Learn")
        for cat, skills in gaps.items():
            with st.expander(cat, expanded=True):
                for s in skills:
                    st.write(f"🔴 {s}")

    # -------- Roadmap --------
    with tab2:
        st.write("### 🎯 Focus Areas")
        st.write(f"- Build strong foundation in **{interest}**")
        if stress == "High":
            st.write("- Manage stress with structured daily routine")
        if communication == "Poor":
            st.write("- Improve communication skills weekly")

    # -------- Week Plan --------
    with tab3:
        for w in week_plan:
            with st.expander(w["title"], expanded=True):
                for p in w["points"]:
                    st.write(f"• {p}")

    # -------- Projects --------
    with tab4:
        st.write("### 🚀 Suggested Projects")
        if interest == "Software Developer":
            st.write("- Student Management System")
            st.write("- Task Tracker App")
            st.write("- Portfolio Website")
        elif interest == "Data Science":
            st.write("- Student Performance Analysis")
            st.write("- Sales Prediction Model")
        else:
            st.write("- Personal Portfolio Website")
            st.write("- CRUD Web Application")

    # -------- Download --------
    roadmap_text = f"""
Personalized Skill Roadmap for {name}
Interest: {interest}
Generated on: {date.today()}

Skills Completed:
{completed}

Skill Gaps:
{gaps}
"""
    st.download_button(
        "⬇️ Download Roadmap",
        roadmap_text,
        file_name="skill_roadmap.txt"
    )

st.divider()

with st.expander("📊 Dataset Preview"):
    st.dataframe(data)

st.caption("Mini Project | Personalized Student Skill Roadmap with Skill Gap Analysis")
