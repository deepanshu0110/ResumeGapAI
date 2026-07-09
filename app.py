"""
app.py — Day 199 polished UI for ResumeGapAI
"""

import streamlit as st
from resumegap_engine import analyze_resume_gap

st.set_page_config(page_title="ResumeGapAI", page_icon="📄", layout="centered")

st.title("📄 ResumeGapAI")
st.markdown("*Paste your resume and a job description to see how well they match.*")

# --------------------------------------------------------------------
# TASK 1 — Input validation & error handling (20 pts)
# --------------------------------------------------------------------
resume = st.text_area("📝 Your Resume", height=200, key="resume_input")
jd = st.text_area("📋 Job Description", height=200, key="jd_input")

# --------------------------------------------------------------------
# TASK 4 — Session state (15 pts)
# --------------------------------------------------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# --------------------------------------------------------------------
# Callback functions for example buttons (fixed Task 5 bug)
# --------------------------------------------------------------------
def load_example_resume(resume_text, jd_text):
    """Set session state values; Streamlit will rerun automatically."""
    st.session_state.resume_input = resume_text
    st.session_state.jd_input = jd_text

# --------------------------------------------------------------------
# Analysis button
# --------------------------------------------------------------------
if st.button("🔍 Analyze", type="primary"):
    if not resume.strip():
        st.warning("⚠️ Please paste your resume text.")
        st.stop()
    if not jd.strip():
        st.warning("⚠️ Please paste the job description text.")
        st.stop()
    if len(resume.split()) < 10:
        st.warning("📏 Resume text looks too short – paste the full resume for an accurate score.")
        st.stop()
    if len(jd.split()) < 10:
        st.warning("📏 Job description looks too short – paste the full JD for an accurate score.")
        st.stop()
    try:
        with st.spinner("Analyzing..."):
            result = analyze_resume_gap(resume, jd)
        st.session_state.last_result = result
    except Exception:
        st.error("❌ Something went wrong. Please check your input and try again.")
        st.stop()

# --------------------------------------------------------------------
# Display results (if any)
# --------------------------------------------------------------------
result = st.session_state.last_result
if result is not None:
    fixed = result['similarity_fixed']
    band = "Strong Match" if fixed >= 70 else "Moderate Match" if fixed >= 45 else "Weak Match"

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🧠 Naive TF‑IDF", f"{result['similarity_naive']:.1f}%")
    with col2:
        st.metric("✅ Corpus‑Corrected TF‑IDF", f"{fixed:.1f}%")
    st.caption("The *Naive* score is shown for transparency; the *Corpus‑Corrected* score is the one to trust.")

    st.write(f"**Match Band:** {band}")
    st.subheader("📌 Top skill gaps to address")
    if result['gap_words']:
        for word in result['gap_words']:
            st.write(f"- {word}")
    else:
        st.info("No significant gaps found – great match!")

    # Downloadable report (Task 3)
    def build_report(res, band):
        lines = ["=== ResumeGapAI Report ===\n"]
        lines.append(f"Corpus‑Corrected Similarity: {res['similarity_fixed']:.1f}%")
        lines.append(f"Naive TF‑IDF Similarity:     {res['similarity_naive']:.1f}%")
        lines.append(f"Match Band:                  {band}")
        lines.append("\nTop skill gaps to address:")
        if res['gap_words']:
            for w in res['gap_words']:
                lines.append(f"  - {w}")
        else:
            lines.append("  None – excellent alignment!")
        return "\n".join(lines)

    report_text = build_report(result, band)
    st.download_button("📥 Download report (.txt)", data=report_text,
                       file_name="resumegap_report.txt", mime="text/plain")

# --------------------------------------------------------------------
# TASK 5 — Sidebar with fixed callback buttons
# --------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ℹ️ About ResumeGapAI")
    st.markdown("ResumeGapAI compares your resume against a job description using "
                "**corpus‑corrected TF‑IDF** and highlights the skills you're missing.")
    st.markdown("[🔗 GitHub Repository](https://github.com/deepanshu0110/ResumeGapAI)")

    st.markdown("---")
    st.markdown("### 🚀 Try an example")

    # Example 1 – Data Analyst
    da_resume = """Data Analyst with 2 years experience in Excel, SQL, and Power BI. Built dashboards for sales tracking and monthly reporting. Skilled in pivot tables, VLOOKUP, and basic Python for data cleaning using pandas. Experience with A/B testing analysis and customer segmentation using Excel. Familiar with Google Sheets and basic statistics."""
    da_jd = """We are looking for a Data Analyst with strong SQL and Python skills. Must have experience building interactive dashboards in Power BI or Tableau. Experience with pandas, statistical analysis, A/B testing, and machine learning is a plus. Knowledge of cloud platforms like AWS or Azure and experience with ETL pipelines is highly desirable. Strong communication skills for presenting insights to stakeholders required."""
    st.button("📊 Load Data Analyst example",
              on_click=load_example_resume, args=(da_resume, da_jd))

    # Example 2 – Data Scientist
    ds_resume = """Data Scientist skilled in Python, scikit-learn, and machine learning including classification, regression, and clustering. Experience with pandas, numpy, and matplotlib for exploratory data analysis. Built predictive models for churn prediction and customer segmentation. Familiar with Jupyter notebooks and Git version control. Basic exposure to SQL."""
    ds_jd = """Seeking a Data Scientist with strong machine learning and deep learning skills. Must know TensorFlow or PyTorch, NLP techniques, and have experience deploying models to production using Docker and cloud platforms like AWS. Experience with MLOps, model monitoring, and A/B testing for model evaluation required. Strong Python and SQL skills essential."""
    st.button("🧠 Load Data Scientist example",
              on_click=load_example_resume, args=(ds_resume, ds_jd))

    # Example 3 – ML Engineer
    ml_resume = """Machine Learning Engineer with experience in Python, TensorFlow, and deploying models using Docker and Flask APIs. Built end-to-end ML pipelines including feature engineering, model training, and monitoring. Experience with AWS, CI/CD, and MLOps practices. Strong background in scikit-learn and PyTorch for production-grade model development."""
    ml_jd = """Looking for a Machine Learning Engineer to build and deploy production ML systems. Requires strong Python, TensorFlow or PyTorch, Docker, Kubernetes, and cloud experience (AWS/GCP). Experience with MLOps, model monitoring, CI/CD pipelines, and A/B testing frameworks required. Knowledge of distributed training and model optimization is a plus."""
    st.button("⚙️ Load ML Engineer example",
              on_click=load_example_resume, args=(ml_resume, ml_jd))

    st.markdown("---")
    st.caption("ResumeGapAI v1.0 • Built with ❤️ for the 100‑Day Challenge")