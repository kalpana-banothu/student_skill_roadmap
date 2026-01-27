import streamlit as st
import pandas as pd
from datetime import date

# ---------------- Page Config ----------------
st.set_page_config(page_title="Student Skill Roadmap", layout="centered")

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    return pd.read_csv("student_performance_extended.csv")  # Replace with your dataset path

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
    if "hostel" in f.columns:
        f["hostel"] = f["hostel"].apply(normalize_yes_no)
    for k, col in [("year", "year"), ("branch", "branch"), ("interest", "interest"), ("skill_level", "skill_level")]:
        if col in f.columns and k in info and info[k] is not None:
            f = f[f[col] == info[k]]
    return f

def build_week_plan(interest, skill_level, budget_level):
    """A structured 4-week roadmap (generic but clean)."""
    free_note = "Use free resources (YouTube/NPTEL/free Coursera audits)." if budget_level=="Low" else "Consider 1 paid course + mentorship for speed."
    if skill_level=="Beginner":
        project = "Mini project: build a basic end-to-end demo"
        depth = "Focus on fundamentals + consistent practice"
    else:
        project = "Project: build a portfolio-grade real-world application"
        depth = "Focus on advanced concepts + real datasets + deployment"
    return [
        {"title":"Week 1 — Foundation","bullets":[f"{depth} in **{interest}** (core concepts).","Set up tools (GitHub, editor, notes).","Daily practice: 45–60 mins.", free_note]},
        {"title":"Week 2 — Skill Building","bullets":["Solve 10–15 practice problems / exercises.","Start a structured course + take notes.","Build 1 small component (feature/module) daily."]},
        {"title":"Week 3 — Projects & Proof","bullets":[project,"Add README + screenshots + clear steps.","Push code daily to GitHub (commit streak)."]},
        {"title":"Week 4 — Career Readiness","bullets":["Resume: add project + skills + links.","Mock interview / presentations (2 sessions).","Polish project + deploy (if possible).","Plan next month based on gaps."]},
    ]

def generate_structured_roadmap(info, df):
    """Return a rich roadmap object (not just flat strings)."""
    steps, risks, habits, goals = [], [], [], []
    sim = get_similar_students(df, info)
    sim_note = None
    if len(sim) >= 5:
        avg_gpa = sim["gpa"].mean() if "gpa" in sim.columns else None
        avg_study = sim["study_hours"].mean() if "study_hours" in sim.columns else None
        if avg_gpa is not None and avg_study is not None:
            sim_note = f"Based on **{len(sim)} similar students** (same year/branch/interest/skill), average GPA is **{avg_gpa:.2f}** and average study hours is **{avg_study:.1f}/day**."
        else:
            sim_note = f"Not enough similar-student rows for strong stats (found {len(sim)}). Using rule-based roadmap."
    # Core goals
    goals.append(f"Build a clear learning path in **{info['interest']}**.")
    if info["gpa"] < 6.0: goals.append("Improve academic consistency (target +0.5 GPA next semester).")
    if info["study_hours"] < 3: goals.append("Increase study hours gradually to a sustainable level.")
    if info["communication"] in ("Poor","Low"): goals.append("Improve communication through weekly speaking/writing practice.")
    # Risks & Habits
    if info["stress_level"]=="High" or info["confusion_level"]=="High":
        risks.append("High stress/confusion can reduce consistency → use weekly planning + short focused sessions.")
        habits.append("10 min breathing/meditation + 25/5 Pomodoro (2 cycles).")
    if info["hostel"]=="Yes":
        habits.append("Hostel routine: fixed sleep + fixed study slot + limit late-night scrolling.")
    else:
        habits.append("Home routine: fixed study slot + communicate study time to family.")
    if info["family_support"]=="Low":
        steps.append("Get external support: mentor/teacher/peer group + online communities.")
    else:
        steps.append("Use family support: share weekly goals and ask for accountability.")
    if info["budget"]=="Low":
        steps.append("Use free resources first + build projects (proof > certificates).")
    else:
        steps.append("Pick 1 high-quality paid course OR mentorship for faster progress.")
    if info["study_hours"]<3:
        steps.append("Study plan: add +30 mins/week until you reach 3–4 hours/day.")
    if info["gpa"]<6.0:
        steps.append("Academics: revise daily + weekly tests + focus on weak subjects.")
    if info["communication"] in ("Poor","Low"):
        steps.append("Communication: 2 short talks/week + write 1 summary/day (5–7 lines).")
    week_plan = build_week_plan(info["interest"], info["skill_level"], info["budget"])
    # Resources by interest
    interest_lower = str(info["interest"]).lower()
    if "data" in interest_lower or "ml" in interest_lower or "ai" in interest_lower:
        resources = ["NPTEL / YouTube: Python + ML basics","Kaggle: datasets + notebooks","GitHub: portfolio + README","LeetCode/HackerRank: fundamentals (optional)"]
        projects = ["Student performance prediction / analysis dashboard","Mini recommender system","Simple ML model + Streamlit deployment"]
    elif "web" in interest_lower:
        resources = ["MDN Web Docs (HTML/CSS/JS)","Frontend practice: small clones","GitHub Pages / Vercel for deployment"]
        projects = ["Portfolio website","To-do app + local storage","Mini full-stack CRUD app"]
    else:
        resources = ["YouTube + NPTEL fundamentals","One structured course (beginner → intermediate)","Build 2–3 projects + document well"]
        projects = ["1 mini project","1 intermediate project","1 portfolio-grade project"]
    return {"similar_note": sim_note,"goals": goals,"risks": risks,"habits": habits,"steps": steps,"week_plan": week_plan,"resources": resources,"projects": projects}

# ---------------- Skill Analysis ----------------
JOB_SKILL_ANALYSIS = {
    "Software Developer": {
        "skills": ["Python / Java","Data Structures & Algorithms","HTML, CSS, JavaScript","Git & GitHub","Databases (SQL)","OOPS","Problem Solving"],
        "projects": ["Student Management System","Task Tracker Application","Portfolio Website","REST API Mini Project"],
        "resources": ["NPTEL – Programming & DSA","YouTube – freeCodeCamp","GeeksForGeeks – DSA","GitHub – Open Source Projects"]
    },
    "Frontend Developer": {
        "skills": ["HTML","CSS","JavaScript","React","Responsive Design","Git & GitHub"],
        "projects": ["Portfolio Website","React To-Do App","UI Clone (Netflix / Amazon)"],
        "resources": ["MDN Web Docs","Traversy Media (YouTube)","React Official Docs"]
    },
    "Data Scientist": {
        "skills": ["Python","Statistics","Pandas & NumPy","Data Visualization","Machine Learning Basics"],
        "projects": ["Student Performance Analysis","Sales Prediction Model","EDA Project"],
        "resources": ["Kaggle Learn","Krish Naik (YouTube)","Coursera ML (Audit Mode)"]
    },
    "AI Engineer": {
        "skills": ["Python","TensorFlow / PyTorch","Machine Learning","Deep Learning","Data Preprocessing","Model Deployment"],
        "projects": ["Image Classification","Chatbot","Recommendation System"],
        "resources": ["Coursera AI Specialization","YouTube Tutorials","Kaggle Competitions"]
    },
    "DevOps Engineer": {
        "skills": ["Linux","Docker","Kubernetes","CI/CD","Cloud (AWS/Azure)","Scripting"],
        "projects": ["Automated Deployment Pipeline","Dockerized Microservices"],
        "resources": ["Udemy DevOps Courses","YouTube Tutorials","AWS Free Tier"]
    }
}

def compute_skill_gap(required_skills, known_skills):
    known = [s for s in required_skills if s in known_skills]
    missing = [s for s in required_skills if s not in known_skills]
    return known, missing

# ---------------- Markdown Export ----------------
def roadmap_to_markdown(name, info, roadmap):
    def s(x): return str(x) if x is not None else ""
    lines = [
        f"# Personalized Roadmap for {s(name)}",
        f"**Generated on:** {date.today()}",
        ""
    ]
    lines.append("## Profile")
    for k in ["year","branch","interest","skill_level","budget","hostel","study_hours",
              "gpa","stress_level","confusion_level","communication","family_support"]:
        lines.append(f"- **{k.replace('_',' ').title()}**: {s(info.get(k))}")
    lines.append("")
    lines.append("## Data Insight")
    lines.append(s(roadmap.get("similar_note","")))
    lines.append("")
    lines.append("## Goals")
    for g in roadmap.get("goals", []): lines.append(f"- {s(g)}")
    lines.append("")
    for section, items in [("Risks to Watch", roadmap.get("risks",[])),
                           ("Daily Habits", roadmap.get("habits",[])),
                           ("Action Steps", roadmap.get("steps",[])),
                           ("Suggested Projects", roadmap.get("projects",[])),
                           ("Resources", roadmap.get("resources",[]))]:
        if items:
            lines.append(f"## {section}")
            for i in items: lines.append(f"- {s(i)}")
            lines.append("")
    # 4-Week plan
    lines.append("## 4-Week Plan")
    for w in roadmap.get("week_plan", []):
        lines.append(f"### {s(w.get('title',''))}")
        for b in w.get("bullets", []):
            lines.append(f"- {s(b)}")
        lines.append("")
    return "\n".join(lines)

# ---------------- UI ----------------
st.title("🎓 Personalized Student Skill Roadmap")
st.caption("A cleaner roadmap output with week-wise plan + data-driven insights.")
st.divider()

# -------- User Input --------
years = safe_unique(data, "year", [1,2,3,4])
branches = safe_unique(data, "branch", ["CSE","IT","ECE","EEE"])
interests = safe_unique(data, "interest", ["Programming","Web","Data Science"])
budgets = safe_unique(data, "budget_level", ["Low","Medium","High"])
skill_levels = safe_unique(data, "skill_level", ["Beginner","Intermediate","Advanced"])
stress_levels = safe_unique(data, "stress_level", ["Low","Medium","High"])
conf_levels = safe_unique(data, "confusion_level", ["Low","Medium","High"])
comm_levels = safe_unique(data, "communication_level", ["Poor","Average","Good"])

st.header("📋 Enter Your Details")
name = st.text_input("Student Name", "")
year = st.selectbox("Year", years)
branch = st.selectbox("Branch", branches)
gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
study_hours = st.slider("Daily Study Hours", 0, 12, 3)
failures = st.number_input("Number of Failures", min_value=0, max_value=10, value=0)
hostel = st.selectbox("Hostel?", ["Yes","No"])
sleep_hours = st.slider("Daily Sleep Hours", 0,12,6)
family_support = st.selectbox("Family Support Level", ["Low","Medium","High"])
interest = st.selectbox("Primary Interest", interests)
budget = st.selectbox("Budget Level", budgets)
skill_level = st.selectbox("Skill Level", skill_levels)
stress_level = st.selectbox("Stress Level", stress_levels)
confusion_level = st.selectbox("Confusion Level", conf_levels)
communication_level = st.selectbox("Communication Level", comm_levels)  # <- consistent name
st.divider()

# -------- Generate Roadmap --------
if st.button("🔍 Generate My Roadmap"):
    student_info = {
        "year": year,"branch": branch,"gpa": float(gpa),"study_hours": int(study_hours),
        "failures": int(failures),"hostel": hostel,"sleep_hours": int(sleep_hours),
        "family_support": family_support,"interest": interest,"budget": budget,
        "skill_level": skill_level,"stress_level": stress_level,"confusion_level": confusion_level,
        "communication": communication_level  # <- consistent key
    }
    roadmap = generate_structured_roadmap(student_info, data)
    st.success(f"✅ Roadmap Generated for {name or 'Student'}")

    # Quick metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", f"{gpa:.1f}")
    col2.metric("Study Hours/day", f"{study_hours}")
    col3.metric("Sleep Hours", f"{sleep_hours}")

    readiness = 0
    readiness += 30 if gpa>=7 else 20 if gpa>=6 else 10
    readiness += 25 if study_hours>=4 else 15 if study_hours>=3 else 8
    readiness += 20 if stress_level!="High" else 8
    readiness += 15 if confusion_level!="High" else 8
    readiness += 10 if communication_level in ("Average","Good") else 5
    readiness = min(readiness,100)
    st.write("### 📈 Readiness Score")
    st.progress(readiness/100)
    st.caption("This score is a UI indicator (not an official assessment).")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧭 Roadmap","🗓️ 4-Week Plan","🧪 Projects","📚 Resources","🧩 Skill Analysis"])
    with tab1:
        st.info(roadmap["similar_note"])
        st.subheader("🎯 Goals")
        for g in roadmap["goals"]: st.write(f"✅ {g}")
        if roadmap["risks"]:
            st.subheader("⚠️ Risks to Watch")
            for r in roadmap["risks"]: st.write(f"• {r}")
        st.subheader("🧠 Daily Habits")
        for h in roadmap["habits"]: st.write(f"🟩 {h}")
        st.subheader("✅ Action Steps")
        for i,s_ in enumerate(roadmap["steps"],1): st.write(f"{i}. {s_}")
    with tab2:
        for w in roadmap["week_plan"]:
            with st.expander(w["title"], expanded=True):
                for b in w["bullets"]: st.write(f"• {b}")
    with tab3:
        st.subheader("Suggested Projects")
        for p in roadmap["projects"]: st.write(f"🚀 {p}")
        st.caption("Tip: Add screenshots + README + clear results.")
    with tab4:
        st.subheader("Recommended Resources")
        for r in roadmap["resources"]: st.write(f"📌 {r}")
    with tab5:
        st.header("🧩 Skill Analysis (Optional)")
        job_choice = st.selectbox("Choose a Job Role", list(JOB_SKILL_ANALYSIS.keys()))
        job_info = JOB_SKILL_ANALYSIS[job_choice]
        c1,c2,c3 = st.columns(3)
        with c1:
            st.subheader("🧠 Skills Required")
            for s_ in job_info["skills"]: st.write("•",s_)
        with c2:
            st.subheader("🧪 Projects")
            for p in job_info["projects"]: st.write("•",p)
        with c3:
            st.subheader("📚 Resources")
            for r in job_info["resources"]: st.write("•",r)
        st.subheader("🎓 Your Current Skills")
        known_skills = st.multiselect("Select skills you already know", job_info["skills"])
        known, missing = compute_skill_gap(job_info["skills"], known_skills)
        st.subheader("📊 Skill Gap Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Skills You Have")
            for s_ in known: st.success(s_) if known else st.warning("No skills selected")
        with col2:
            st.markdown("### ❌ Skills You Need to Learn")
            for s_ in missing: st.error(s_)
        st.subheader("🛣️ Recommended Learning Order")
        for i,s_ in enumerate(missing,1): st.write(f"{i}. Learn **{s_}**")

    # Download markdown
    md = roadmap_to_markdown(name, student_info, roadmap)
    st.download_button(label="⬇️ Download Roadmap (Markdown)",
                       data=md.encode("utf-8"),
                       file_name=f"roadmap_{(name or 'student').replace(' ','_').lower()}.md",
                       mime="text/markdown")

st.divider()
with st.expander("📊 Sample Student Dataset (Preview)", expanded=False):
    st.dataframe(data, use_container_width=True)
st.caption("Mini Project | Student Skill Roadmap | Streamlit Web App")
