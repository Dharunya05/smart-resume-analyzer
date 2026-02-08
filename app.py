import streamlit as st
import pdfplumber
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9+.# ]', '', text)
    return text.lower()

def extract_skills(text):
    skills_list = [
        "python", "sql", "power bi", "excel",
        "machine learning", "data science",
        "artificial intelligence", "statistics"
    ]
    return [skill.upper() for skill in skills_list if skill in text]

def skill_gap_analysis(resume_skills, job_skills):
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched = sorted(resume_set.intersection(job_set))
    missing = sorted(job_set - resume_set)

    return matched, missing

def calculate_match_score(matched, total):
    if total == 0:
        return 0
    return round((len(matched) / total) * 100, 2)

learning_roadmap = {
    "deep learning": [
        "Neural Networks basics",
        "CNN & RNN",
        "PyTorch / TensorFlow projects"
    ],
    "statistics": [
        "Probability",
        "Hypothesis Testing",
        "Regression Analysis"
    ],
    "tableau": [
        "Basic Charts",
        "Dashboards",
        "Mini Projects"
    ]
}

st.title("📄 Smart Resume Analyzer & Skill Gap Detector")

st.markdown("""
### 🔍 What this app does
Upload your resume and compare it with a job description to:
- Extract technical skills from your resume
- Identify matched and missing skills
- Calculate resume–job match percentage
- Get a personalized learning roadmap

### 📌 Instructions
1. Upload a **text-based PDF resume**
2. Paste the **Job Description**
3. View skill analysis and recommendations
""")

st.info("ℹ️ Note: Currently supports text-based resumes. Scanned/image-based resumes will be added in future versions.")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description")

if uploaded_file and not job_desc.strip():
    st.warning("⚠️ Please paste a Job Description to continue.")
    st.stop()

if uploaded_file and job_desc:

    progress = st.progress(0)
    status = st.empty()

    # Step 1: Read resume
    status.info("📄 Reading resume...")
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_text = clean_text(resume_text)
    progress.progress(30)

    if not resume_text.strip():
        st.error("❌ No readable text found in the resume. Please upload a text-based PDF.")
        st.stop()

    # Step 2: Extract skills
    status.info("🧠 Extracting skills...")
    resume_skills = extract_skills(resume_text)
    progress.progress(60)

    if not resume_skills:
        st.warning("⚠️ No matching technical skills found in the resume.")

    # Step 3: Compare skills
    status.info("📊 Comparing with job description...")
    job_skills = [
        "python", "sql", "machine learning",
        "deep learning", "tableau", "statistics"
    ]

    matched, missing = skill_gap_analysis(resume_skills, job_skills)
    score = calculate_match_score(matched, len(job_skills))
    progress.progress(100)

    status.success("✅ Analysis completed!")
    st.divider()

    # Output section
    st.subheader("🛠️ Extracted Skills")
    st.write(", ".join(resume_skills) if resume_skills else "No skills detected")

    st.subheader("📈 Resume Match Score")
    st.metric(label="Match Percentage", value=f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Matched Skills")
        if matched:
            st.success(", ".join(s.upper() for s in matched))
        else:
            st.write("No matched skills found")

    with col2:
        st.subheader("🔴 Missing Skills")
        if missing:
            st.error(", ".join(s.upper() for s in missing))
        else:
            st.write("No missing skills 🎉")

    st.subheader("📘 Learning Roadmap")
    for skill in missing:
        if skill in learning_roadmap:
            st.markdown(f"**{skill.upper()}**")
            for step in learning_roadmap[skill]:
                st.write("•", step)
