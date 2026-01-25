# import streamlit as st
# import pandas as pd

# # --- Page configuration ---
# st.set_page_config(
#     page_title="Student Skill Roadmap",
#     layout="centered"
# )

# # --- Load dataset ---
# @st.cache_data
# def load_data():
#     return pd.read_csv("student_performance_extended.csv")  # your dataset filename

# data = load_data()

# # --- Title ---
# st.title("🎓 Personalized Student Skill Roadmap Web App")
# st.write("Interactive web application to guide students in planning their skills, career, and personal development.")

st.divider()

# --- User Input ---
# st.header("📋 Enter Your Details")

# name = st.text_input("Student Name", "")
# year = st.selectbox("Year", sorted(data["year"].unique()))
# branch = st.selectbox("Branch", sorted(data["branch"].unique()))
# gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
# study_hours = st.slider("Daily Study Hours", 0, 12, 3)
# failures = st.number_input("Number of Failures", min_value=0, max_value=10, value=0)
# hostel = st.selectbox("Hostel?", ["Yes", "No"])
# sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 6)
# family_support = st.selectbox("Family Support Level", ["Low", "Medium", "High"])
# interest = st.selectbox("Primary Interest", sorted(data["interest"].unique()))
# budget = st.selectbox("Budget Level", sorted(data["budget_level"].unique()))
# skill_level = st.selectbox("Skill Level", sorted(data["skill_level"].unique()))
# stress_level = st.selectbox("Stress Level", sorted(data["stress_level"].unique()))
# confusion_level = st.selectbox("Confusion Level", sorted(data["confusion_level"].unique()))
# communication = st.selectbox("Communication Level", sorted(data["communication_level"].unique()))

# st.divider()

# # --- Recommendation Logic ---
# def generate_roadmap(info):
#     steps = []

#     # Skill improvement
#     if info['skill_level'] == "Beginner":
#         steps.append("Start with basics of your interest area and practice small projects.")
#     else:
#         steps.append("Focus on advanced projects, real-world applications, and certifications.")

#     # Study & GPA
#     if info['study_hours'] < 3 or info['gpa'] < 6.0:
#         steps.append("Increase study hours and follow a structured learning schedule.")

#     # Hostel / Sleep
    # if info['hostel'] == "Yes":
    #     steps.append("Maintain a healthy routine: proper sleep, food, and time management in hostel.")
    # else:
    #     steps.append("Balance family responsibilities with studies and skill building.")

    # # Stress & Confusion
    # if info['stress_level'] == "High" or info['confusion_level'] == "High":
    #     steps.append("Adopt stress management techniques: meditation, time management, and counseling.")

    # # Family Support
    # if info['family_support'] == "Low":
    #     steps.append("Seek mentors, peer groups, or online communities for guidance.")

    # # Communication
    # if info['communication'] == "Poor":
    #     steps.append("Work on communication skills through speaking, writing, and online workshops.")

    # # Interest-based learning
#     steps.append(f"Follow curated courses, books, and online tutorials for {info['interest']}.")

#     # Budget
#     if info['budget'] == "Low":
#         steps.append("Use free resources: YouTube tutorials, free MOOCs, and open-source materials.")
#     else:
#         steps.append("Consider paid courses, mentorship, or workshops for faster learning.")

#     return steps

# # --- Generate Roadmap Button ---
# if st.button("🔍 Generate My Roadmap"):
#     student_info = {
#         'skill_level': skill_level,
    #     'interest': interest,
    #     'study_hours': study_hours,
    #     'gpa': gpa,
    #     'stress_level': stress_level,
    #     'confusion_level': confusion_level,
    #     'hostel': hostel,
    #     'communication': communication,
    #     'budget': budget,
    #     'family_support': family_support
    # }

    # roadmap = generate_roadmap(student_info)
    # st.success(f"✅ Roadmap Generated for {name}")
    
#     st.subheader("📌 Suggested Steps:")
#     for i, step in enumerate(roadmap, 1):
#         st.write(f"{i}. {step}")

#     st.subheader("📚 Recommended Resources:")
#     st.markdown("""
#     - **Free Courses:** YouTube, NPTEL, Coursera free courses  
#     - **Paid Courses:** Udemy, Coursera, edX  
#     - **Practice & Projects:** HackerRank, LeetCode, GitHub  
#     - **Soft Skills & Communication:** Toastmasters, online workshops
#     """)

# st.divider()

# # --- Display Dataset Preview ---
# st.header("📊 Sample Student Dataset")
# st.dataframe(data)

# st.caption("Mini Project | Student Skill Roadmap | Streamlit Web App")
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

def normalize_yes_no(x):
    if isinstance(x, str):
        x = x.strip().lower()
        if x in ("yes", "y", "true", "1"):
            return "Yes"
    return "No"

def get_similar_students(df, info):
    """Simple similarity filter (no ML): same year + branch + interest + skill_level if possible."""
    f = df.copy()

    # Normalize columns if present
    if "hostel" in f.columns:
        f["hostel"] = f["hostel"].apply(normalize_yes_no)

    # Apply filters only if columns exist
    for k, col in [
        ("year", "year"),
        ("branch", "branch"),
        ("interest", "interest"),
        ("skill_level", "skill_level"),
    ]:
        if col in f.columns and k in info and info[k] is not None:
            f = f[f[col] == info[k]]

    return f

def build_week_plan(interest, skill_level, budget_level):
    """A structured 4-week roadmap (generic but clean)."""
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

def generate_structured_roadmap(info, df):
    """Return a rich roadmap object (not just flat strings)."""
    steps = []
    risks = []
    habits = []
    goals = []

    # --- Data-driven insights from similar students ---
    sim = get_similar_students(df, info)
    sim_note = None
    if len(sim) >= 5:
        # Try to use columns if present
        avg_gpa = sim["gpa"].mean() if "gpa" in sim.columns else None
        avg_study = sim["study_hours"].mean() if "study_hours" in sim.columns else None
        if avg_gpa is not None and avg_study is not None:
            sim_note = f"Based on **{len(sim)} similar students** (same year/branch/interest/skill), average GPA is **{avg_gpa:.2f}** and average study hours is **{avg_study:.1f}/day**."
    else:
        sim_note = f"Not enough similar-student rows for strong stats (found {len(sim)}). Using rule-based roadmap."

    # --- Core goals ---
    goals.append(f"Build a clear learning path in **{info['interest']}**.")
    if info["gpa"] < 6.0:
        goals.append("Improve academic consistency (target +0.5 GPA in next semester).")
    if info["study_hours"] < 3:
        goals.append("Increase study hours gradually to a sustainable level.")
    if info["communication"] in ("Poor", "Low"):
        goals.append("Improve communication through weekly speaking/writing practice.")

    # --- Risks & fixes ---
    if info["stress_level"] == "High" or info["confusion_level"] == "High":
        risks.append("High stress/confusion can reduce consistency → use weekly planning + short focused sessions.")
        habits.append("10 min breathing/meditation + 25/5 Pomodoro (2 cycles).")

    if info["hostel"] == "Yes":
        habits.append("Hostel routine: fixed sleep + fixed study slot + limit late-night scrolling.")
    else:
        habits.append("Home routine: fixed study slot + communicate study time to family.")

    if info["family_support"] == "Low":
        steps.append("Get external support: mentor/teacher/peer group + online communities.")
    else:
        steps.append("Use family support: share weekly goals and ask for accountability.")

    if info["budget"] == "Low":
        steps.append("Use free resources first + build projects (proof > certificates).")
    else:
        steps.append("Pick 1 high-quality paid course OR mentorship for faster progress.")

    # --- Study upgrade ---
    if info["study_hours"] < 3:
        steps.append("Study plan: add +30 mins/week until you reach 3–4 hours/day.")
    if info["gpa"] < 6.0:
        steps.append("Academics: revise daily + weekly tests + focus on weak subjects.")

    # --- Communication ---
    if info["communication"] in ("Poor", "Low"):
        steps.append("Communication: 2 short talks/week + write 1 summary/day (5–7 lines).")

    week_plan = build_week_plan(info["interest"], info["skill_level"], info["budget"])

    # --- Resources by interest (simple mapping) ---
    interest_lower = str(info["interest"]).lower()
    if "data" in interest_lower or "ml" in interest_lower or "ai" in interest_lower:
        resources = [
            "NPTEL / YouTube: Python + ML basics",
            "Kaggle: datasets + notebooks",
            "GitHub: portfolio + README",
            "LeetCode/HackerRank: fundamentals (optional)",
        ]
        projects = [
            "Student performance prediction / analysis dashboard",
            "Mini recommender system",
            "Simple ML model + Streamlit deployment",
        ]
    elif "web" in interest_lower:
        resources = [
            "MDN Web Docs (HTML/CSS/JS)",
            "Frontend practice: small clones",
            "GitHub Pages / Vercel for deployment",
        ]
        projects = [
            "Portfolio website",
            "To-do app + local storage",
            "Mini full-stack CRUD app",
        ]
    else:
        resources = [
            "YouTube + NPTEL fundamentals",
            "One structured course (beginner → intermediate)",
            "Build 2–3 projects + document well",
        ]
        projects = [
            "1 mini project",
            "1 intermediate project",
            "1 portfolio-grade project",
        ]

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
    lines = []
    lines.append(f"# Personalized Roadmap for {name or 'Student'}")
    lines.append(f"**Generated on:** {date.today().isoformat()}")
    lines.append("")
    lines.append("## Profile")
    for k in ["year", "branch", "interest", "skill_level", "budget", "hostel", "study_hours", "gpa", "stress_level", "confusion_level", "communication", "family_support"]:
        lines.append(f"- **{k.replace('_',' ').title()}**: {info.get(k)}")
    lines.append("")
    lines.append("## Data Insight")
    lines.append(roadmap["similar_note"])
    lines.append("")
    lines.append("## Goals")
    for g in roadmap["goals"]:
        lines.append(f"- {g}")
    lines.append("")
    if roadmap["risks"]:
        lines.append("## Risks to Watch")
        for r in roadmap["risks"]:
            lines.append(f"- {r}")
        lines.append("")
    lines.append("## Daily Habits")
    for h in roadmap["habits"]:
        lines.append(f"- {h}")
    lines.append("")
    lines.append("## Action Steps")
    for s in roadmap["steps"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## 4-Week Plan")
    for w in roadmap["week_plan"]:
        lines.append(f"### {w['title']}")
        for b in w["bullets"]:
            lines.append(f"- {b}")
        lines.append("")
    lines.append("## Suggested Projects")
    for p in roadmap["projects"]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("## Resources")
    for r in roadmap["resources"]:
        lines.append(f"- {r}")
    lines.append("")
    return "\n".join(lines)

# ---------------- UI ----------------
st.title("🎓 Personalized Student Skill Roadmap")
st.caption("A cleaner roadmap output with week-wise plan + data-driven insights.")
st.divider()

st.header("📋 Enter Your Details")

# Pick options safely (won't crash if columns missing)
years = safe_unique(data, "year", [1, 2, 3, 4])
branches = safe_unique(data, "branch", ["CSE", "IT", "ECE", "EEE"])
interests = safe_unique(data, "interest", ["ML", "Web", "DSA"])
budgets = safe_unique(data, "budget_level", ["Low", "Medium", "High"])
skill_levels = safe_unique(data, "skill_level", ["Beginner", "Intermediate", "Advanced"])
stress_levels = safe_unique(data, "stress_level", ["Low", "Medium", "High"])
conf_levels = safe_unique(data, "confusion_level", ["Low", "Medium", "High"])
comm_levels = safe_unique(data, "communication_level", ["Poor", "Average", "Good"])

name = st.text_input("Student Name", "")
year = st.selectbox("Year", years)
branch = st.selectbox("Branch", branches)
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Daily Study Hours", 0, 12, 3)
failures = st.number_input("Number of Failures", min_value=0, max_value=10, value=0)
hostel = st.selectbox("Hostel?", ["Yes", "No"])
sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 6)
family_support = st.selectbox("Family Support Level", ["Low", "Medium", "High"])
interest = st.selectbox("Primary Interest", interests)
budget = st.selectbox("Budget Level", budgets)
skill_level = st.selectbox("Skill Level", skill_levels)
stress_level = st.selectbox("Stress Level", stress_levels)
confusion_level = st.selectbox("Confusion Level", conf_levels)
communication = st.selectbox("Communication Level", comm_levels)

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

    roadmap = generate_structured_roadmap(student_info, data)

    st.success(f"✅ Roadmap Generated for {name or 'Student'}")

    # Quick dashboard metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", f"{gpa:.1f}")
    col2.metric("Study Hours/day", f"{study_hours}")
    col3.metric("Sleep Hours", f"{sleep_hours}")

    # A simple "readiness" score (just UI)
    readiness = 0
    readiness += 30 if gpa >= 7 else 20 if gpa >= 6 else 10
    readiness += 25 if study_hours >= 4 else 15 if study_hours >= 3 else 8
    readiness += 20 if stress_level != "High" else 8
    readiness += 15 if confusion_level != "High" else 8
    readiness += 10 if communication in ("Average", "Good") else 5
    readiness = min(readiness, 100)

    st.write("### 📈 Readiness Score")
    st.progress(readiness / 100)
    st.caption("This score is a UI indicator (not an official assessment).")

    tab1, tab2, tab3, tab4 = st.tabs(["🧭 Roadmap", "🗓️ 4-Week Plan", "🧪 Projects", "📚 Resources"])

    with tab1:
        st.info(roadmap["similar_note"])
        st.subheader("🎯 Goals")
        for g in roadmap["goals"]:
            st.write(f"✅ {g}")

        if roadmap["risks"]:
            st.subheader("⚠️ Risks to Watch")
            for r in roadmap["risks"]:
                st.write(f"• {r}")

        st.subheader("🧠 Daily Habits")
        for h in roadmap["habits"]:
            st.write(f"🟩 {h}")

        st.subheader("✅ Action Steps")
        for i, s in enumerate(roadmap["steps"], 1):
            st.write(f"{i}. {s}")

    with tab2:
        for w in roadmap["week_plan"]:
            with st.expander(w["title"], expanded=True):
                for b in w["bullets"]:
                    st.write(f"• {b}")

    with tab3:
        st.subheader("Suggested Projects")
        for p in roadmap["projects"]:
            st.write(f"🚀 {p}")
        st.caption("Tip: Add screenshots + README + clear results. That makes your project look strong.")

    with tab4:
        st.subheader("Recommended Resources")
        for r in roadmap["resources"]:
            st.write(f"📌 {r}")

    # Download as markdown
    md = roadmap_to_markdown(name, student_info, roadmap)
    st.download_button(
        label="⬇️ Download Roadmap (Markdown)",
        data=md.encode("utf-8"),
        file_name=f"roadmap_{(name or 'student').replace(' ','_').lower()}.md",
        mime="text/markdown",
    )

    st.divider()

# ---------------- Dataset preview ----------------
with st.expander("📊 Sample Student Dataset (Preview)", expanded=False):
    st.dataframe(data, use_container_width=True)

st.caption("Mini Project | Student Skill Roadmap | Streamlit Web App")





