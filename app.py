import streamlit as st

st.set_page_config(page_title="Student Skill Roadmap", layout="wide")

st.title("🎓 Student Skill Roadmap Dashboard")

st.image("vitaly-gariev-Sc2iIlwScic-unsplash.jpg", use_column_width=True)

if st.button("Start Your Roadmap"):
    st.switch_page("1_Student_Roadmap")
