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

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_text = clean_text(resume_text)

    resume_skills = extract_skills(resume_text)

    job_skills = [
        "python", "sql", "machine learning",
        "deep learning", "tableau", "statistics"
    ]

    matched, missing = skill_gap_analysis(resume_skills, job_skills)
    score = calculate_match_score(matched, len(job_skills))

    st.subheader("✅ Extracted Skills")
    st.write(resume_skills)

    st.subheader("📊 Resume Match Score")
    st.success(f"{score}% Match")

    st.subheader("🟢 Matched Skills")
    st.write([s.upper() for s in matched])

    st.subheader("🔴 Missing Skills")
    st.write([s.upper() for s in missing])

    st.subheader("📘 Learning Roadmap")
    for skill in missing:
        if skill in learning_roadmap:
            st.markdown(f"**{skill.upper()}**")
            for step in learning_roadmap[skill]:
                st.write("•", step)
