import streamlit as st
import pandas as pd
from datetime import date

# ---------------- Page config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")

# ---------------- Load dataset ----------------
@st.cache_data
def load_data():
    return pd.read_csv("student_performance_extended.csv")

data = load_data()

# ---------------- Helpers ----------------
def safe_unique(df, col, fallback):
    return sorted(df[col].dropna().unique()) if col in df.columns else fallback

# ---------------- Roadmap Logic ----------------
def generate_structured_roadmap(info, df):
    steps = []
    risks = []
    habits = []
    goals = []

    # Similar students insights
    sim = df.copy()
    for k, col in [("year","year"),("branch","branch"),("interest","interest"),("skill_level","skill_level")]:
        if col in sim.columns and k in info and info[k] is not None:
            sim = sim[sim[col]==info[k]]
    sim_note = f"Found {len(sim)} similar students for reference." if len(sim) else "No similar students data available."

    # Goals
    goals.append(f"Focus on **{info['interest']}** learning path.")
    if info['gpa']<6.0: goals.append("Improve GPA to 6.0+")
    if info['study_hours']<3: goals.append("Increase study hours")

    # Risks
    if info["stress_level"]=="High" or info["confusion_level"]=="High":
        risks.append("High stress/confusion can reduce learning effectiveness.")
    if info["communication"] in ("Poor","Low"):
        steps.append("Improve communication skills.")

    # Habits
    habits.append("Daily study & practice sessions.")
    habits.append("Use free resources if budget is low.")

    # Steps
    steps.append("Follow structured weekly roadmap.")
    steps.append("Build projects to demonstrate learning.")

    # 4-week roadmap
    week_plan = [
        {"title":"Week 1 - Basics","bullets":[f"Learn core concepts of {info['interest']}", "Practice exercises", "Setup tools"]},
        {"title":"Week 2 - Intermediate","bullets":["Small project", "Take notes", "Daily exercises"]},
        {"title":"Week 3 - Advanced","bullets":["Portfolio project", "Documentation", "GitHub push"]},
        {"title":"Week 4 - Career Readiness","bullets":["Resume building","Mock interviews","Deploy project"]}
    ]

    # Resources & Projects based on interest
    interest_lower = info['interest'].lower()
    if "web" in interest_lower:
        resources = ["MDN Web Docs","freeCodeCamp","GitHub Pages"]
        projects = ["Portfolio website","To-do app","Mini full-stack CRUD app"]
    elif "data" in interest_lower or "ml" in interest_lower:
        resources = ["Kaggle Learn","YouTube ML tutorials","GitHub projects"]
        projects = ["Student performance prediction","Mini ML model","EDA project"]
    else:
        resources = ["YouTube tutorials","Open courses","Mini projects"]
        projects = ["Small demo project","Portfolio project"]

    return {
        "similar_note": sim_note,
        "goals": goals,
        "risks": risks,
        "habits": habits,
        "steps": steps,
        "week_plan": week_plan,
        "resources": resources,
        "projects": projects,
    }

def roadmap_to_markdown(name, info, roadmap):
    def s(x): return str(x) if x is not None else ""
    lines = [f"# Personalized Roadmap for {s(name)}", f"**Generated on:** {date.today]()
