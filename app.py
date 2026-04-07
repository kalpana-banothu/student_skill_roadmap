import streamlit as st

st.set_page_config(page_title="Student Skill Roadmap", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    st.title("🎓 Student Skill Roadmap Dashboard")

    st.image("vitaly-gariev-Sc2iIlwScic-unsplash.jpg", use_column_width=True)

    if st.button("Start Your Roadmap"):
        st.session_state.page = "roadmap"
        st.rerun()

# ---------------- ROADMAP PAGE ----------------
elif st.session_state.page == "roadmap":
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
        "Backend Developer": {
            "skills": [
                "Node.js / Python / Java",
                "Databases (SQL/NoSQL)",
                "APIs / RESTful Services",
                "Git & GitHub",
                "Authentication & Security"
            ],
            "projects": [
                "REST API Project",
                "E-commerce Backend",
                "Blog Platform Backend"
            ],
            "resources": [
                "Udemy Backend Courses",
                "YouTube - Tech With Tim / Traversy Media",
                "MongoDB University"
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
        },
        "Machine Learning Engineer": {
            "skills": [
                "Python",
                "Linear Algebra & Statistics",
                "Scikit-learn / TensorFlow / PyTorch",
                "Data Preprocessing",
                "Model Deployment"
            ],
            "projects": [
                "Predictive Analytics Model",
                "Image Classification Project",
                "Recommendation System"
            ],
            "resources": [
                "Fast.ai Courses",
                "DeepLearning.ai (Coursera)",
                "YouTube - Sentdex / Krish Naik"
            ]
        },
        "DevOps Engineer": {
            "skills": [
                "Linux / Shell Scripting",
                "CI/CD (Jenkins/GitHub Actions)",
                "Docker / Kubernetes",
                "Cloud Platforms (AWS / GCP / Azure)",
                "Monitoring & Logging"
            ],
            "projects": [
                "CI/CD Pipeline Setup",
                "Dockerized Application Deployment",
                "Cloud Infrastructure Project"
            ],
            "resources": [
                "Linux Academy / A Cloud Guru",
                "YouTube - TechWorld with Nana",
                "Official Docker & Kubernetes Docs"
            ]
        },
        "UI/UX Designer": {
            "skills": [
                "Figma / Adobe XD",
                "Wireframing & Prototyping",
                "User Research & Testing",
                "Responsive Design Principles",
                "Portfolio Creation"
            ],
            "projects": [
                "Mobile App Wireframes",
                "Website Redesign Project",
                "Interactive Prototype"
            ],
            "resources": [
                "Figma Learn Tutorials",
                "Coursera UI/UX Courses",
                "YouTube - DesignCourse / CharliMarieTV"
            ]
        },
        "Cybersecurity Analyst": {
            "skills": [
                "Networking Basics",
                "Linux & Windows Security",
                "Penetration Testing",
                "Firewalls & IDS/IPS",
                "Security Tools (Wireshark, Nmap)"
            ],
            "projects": [
                "Vulnerability Assessment",
                "Phishing Simulation",
                "Secure Web Application Setup"
            ],
            "resources": [
                "TryHackMe / Hack The Box",
                "Cybrary Courses",
                "YouTube - NetworkChuck / The Cyber Mentor"
            ]
        },
        "Mobile App Developer": {
            "skills": [
                "Java / Kotlin / Swift / Flutter",
                "UI/UX for Mobile",
                "APIs & Backend Integration",
                "App Deployment (Play Store / App Store)",
                "Debugging & Testing"
            ],
            "projects": [
                "Todo App",
                "Weather Forecast App",
                "E-commerce Mobile App"
            ],
            "resources": [
                "Udemy Mobile App Courses",
                "YouTube - CodeWithChris / The Net Ninja",
                "Official Flutter Docs"
            ]
        },
        "Cloud Engineer": {
            "skills": [
                "AWS / Azure / GCP",
                "Cloud Architecture & Design",
                "Networking & Security",
                "CI/CD Pipelines",
                "Infrastructure as Code (Terraform)"
            ],
            "projects": [
                "Deploy Web App on Cloud",
                "Serverless Application Project",
                "Cloud Monitoring Setup"
            ],
            "resources": [
                "AWS / Azure / GCP Official Docs",
                "A Cloud Guru Courses",
                "YouTube - TechWorld with Nana"
            ]
        },
        "Business Analyst": {
            "skills": [
                "Excel / SQL / Tableau / PowerBI",
                "Requirement Gathering",
                "Process Modeling",
                "Data Analysis & Reporting",
                "Communication & Presentation"
            ],
            "projects": [
                "Sales Dashboard",
                "Customer Analysis Report",
                "Process Optimization Project"
            ],
            "resources": [
                "Coursera Business Analytics",
                "Udemy SQL / Tableau Courses",
                "YouTube - Analytics University"
            ]
        },
        "Digital Marketing Specialist": {
            "skills": [
                "SEO / SEM",
                "Google Analytics",
                "Content Creation",
                "Social Media Marketing",
                "Email Marketing"
            ],
            "projects": [
                "SEO Campaign Project",
                "Social Media Ad Campaign",
                "Email Marketing Automation"
            ],
            "resources": [
                "Google Digital Garage",
                "HubSpot Academy",
                "YouTube - Neil Patel / Brian Dean"
            ]
        },
        "Blockchain Developer": {
            "skills": [
                "Solidity / Ethereum",
                "Smart Contracts",
                "Web3.js / Ethers.js",
                "Blockchain Architecture",
                "Cryptography Basics"
            ],
            "projects": [
                "Smart Contract Deployment",
                "NFT Minting Platform",
                "Decentralized App (DApp)"
            ],
            "resources": [
                "CryptoZombies.io",
                "Coursera Blockchain Courses",
                "YouTube - Dapp University"
            ]
        },
        "AI Researcher": {
            "skills": [
                "Python / R",
                "Mathematics (Linear Algebra, Probability)",
                "Deep Learning",
                "NLP / Computer Vision",
                "Research Paper Reading & Implementation"
            ],
            "projects": [
                "Image Captioning Model",
                "Text Summarization Model",
                "Custom Neural Network Research"
            ],
            "resources": [
                "arXiv Papers",
                "DeepLearning.ai",
                "YouTube - Yannic Kilcher / Two Minute Papers"
            ]
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
    st.header("📋 Enter Your Details")

# --- Row 1: Basic Info ---
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Student Name", "")
with col2:
    year = st.selectbox("Year", 1,2,3,4)
with col3:
    branch = st.selectbox("Branch", "CSE","ECE","EEE","MECHANICAL","CSD","AIML")

# --- Row 2: Academic Performance ---
col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    gpa = st.slider("GPA", 0.0, 10.0, 7.0, 0.1)
with col_a2:
    study_hours = st.slider("Daily Study Hours", 0, 12, 3)
with col_a3:
    backlogs = st.number_input("Number of Backlogs", min_value=0, max_value=10, value=0)

# --- Row 3: Environment & Lifestyle ---
col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    hostel = st.selectbox("Hostel?", ["Yes","No"])
with col_l2:
    sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 6)
with col_l3:
    family_support = st.selectbox("Family Support Level", ["Low","Medium","High"])

st.divider()

# THIS LINE MUST NOT HAVE EXTRA SPACES AT THE START
if st.button("🔍 Generate My Roadmap"):
    # Everything inside the button must be indented exactly 4 spaces
    st.write(f"Generating roadmap for {name}...")
    # call your roadmap function here

 
    # ---------------- Skill Analysis Section (Standalone) ----------------
    st.divider()
    st.header("🧩 Skill Analysis (Optional / Standalone)")
    
    # User selects a job role first
    job_choice = st.selectbox("Choose a Job Role", ["Select a role"] + list(JOB_SKILL_ANALYSIS.keys()), key="skill_analysis_role")
    
    if job_choice != "Select a role":
        job_info = JOB_SKILL_ANALYSIS[job_choice]
    
        st.subheader("🧠 Required Skills")
        st.write(", ".join(job_info["skills"]))
    
        st.subheader("🧪 Sample Projects")
        for p in job_info["projects"]:
            st.write(f"• {p}")
    
        st.subheader("📚 Recommended Resources")
        for r in job_info["resources"]:
            st.write(f"• {r}")
    
        st.subheader("🎓 Your Current Skills")
        known_skills = st.multiselect("Select skills you already know", job_info["skills"], key="skill_analysis_known")
    
        # Only show skill gap analysis if user selects known skills
        if known_skills:
            known, missing = compute_skill_gap(job_info["skills"], known_skills)
    
            st.subheader("📊 Skill Gap Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### ✅ Skills You Have")
                for s in known:
                    st.success(s)
    
            with col2:
                st.markdown("### ❌ Skills You Need to Learn")
                for s in missing:
                    st.error(s)
    
            if missing:
                st.subheader("🛣️ Recommended Learning Order")
                for i, s in enumerate(missing, 1):
                    st.write(f"{i}. Learn **{s}**")
    
    
    
    # ---------------- Dataset Preview ----------------
    st.divider()
    with st.expander("📊 Sample Student Dataset (Preview)", expanded=False):
        st.dataframe(data, use_container_width=True)
    st.caption("Mini Project | Student Skill Roadmap | Streamlit Web App")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()








