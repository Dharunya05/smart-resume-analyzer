import streamlit as st
import pdfplumber
import re

from pdf2image import convert_from_bytes
import pytesseract

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_with_ocr(uploaded_file, max_pages=5):
    try:
        images = convert_from_bytes(uploaded_file.read())

        ocr_text = ""
        for i, image in enumerate(images):
            if i >= max_pages:
                break
            page_text = pytesseract.image_to_string(image, lang="eng")
            ocr_text += page_text + "\n"

        return ocr_text

    except Exception as e:
        return ""

def get_resume_text(uploaded_file):
    text = extract_text_from_pdf(uploaded_file)

    if not text or len(text.strip()) < 100:
        return None, "ocr"

    return text, "pdf"

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

def skill_frequency(text, skills):
    frequency = {}
    for skill in skills:
        count = text.count(skill.lower())
        frequency[skill.upper()] = count
    return frequency

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

def get_skill_strength(count):
    if count >= 4:
        return "High"
    elif count >= 2:
        return "Medium"
    else:
        return "Low"

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
    resume_text, method = get_resume_text(uploaded_file)

    if method == "ocr":
        status.warning("🖼️ Scanned resume detected.")
        status.info("🔍 Trying OCR extraction...")
        resume_text = extract_text_with_ocr(uploaded_file)

    resume_text = clean_text(resume_text)
    progress.progress(30)
    
    # Step 1.5: Validate extracted text
    if not resume_text or not resume_text.strip():
        st.error("❌ Unable to extract readable text from resume.")
        st.info("Try uploading a clearer PDF or a text-based resume.")
        st.stop()

    # Step 2: Extract skills
    status.info("🧠 Extracting skills...")
    resume_skills = extract_skills(resume_text)
    skill_freq = skill_frequency(resume_text, resume_skills)
    progress.progress(60)

    if not resume_skills:
        st.warning("⚠️ No matching technical skills found in the resume.")

    # Step 3: Compare skills
    status.info("📊 Comparing with job description...")

    job_desc_clean = clean_text(job_desc)
    job_skills = extract_skills(job_desc_clean)

    if not job_skills:
        st.error("❌ No recognizable skills found in Job Description.")
        st.stop()

    from collections import Counter
    job_skill_counts = {}
    for skill in job_skills:
        job_skill_counts[skill] = job_desc_clean.count(skill.lower())

    matched, missing = skill_gap_analysis(resume_skills, job_skills)
    score = calculate_match_score(matched, len(job_skills))
    progress.progress(100)

    status.success("✅ Analysis completed!")
    st.divider()

    # Output section
    st.subheader("🛠️ Extracted Skills")

    if resume_skills:
        for skill in resume_skills:
            st.write("•", skill)
    else:
        st.write("No skills detected")
    
    st.subheader("💪 Skill Strength Analysis")

    for skill, count in skill_freq.items():
        strength = get_skill_strength(count)

        if strength == "High":
            st.success(f"{skill} → {strength} ({count} mentions)")
        elif strength == "Medium":
            st.info(f"{skill} → {strength} ({count} mentions)")
        else:
            st.warning(f"{skill} → {strength} ({count} mentions)")

    st.subheader("📈 Resume Match Score")
    st.metric(label="Match Percentage", value=f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Matched Skills")
        if matched:
            for skill in matched:
                st.success(skill.upper())
        else:
            st.write("No matched skills found")

    with col2:
        st.subheader("🔴 Missing Skills")
        if missing:
            for skill in missing:
                st.error(skill.upper())
        else:
            st.write("No missing skills 🎉")

    st.subheader("📊 Skill Coverage Visualization")
    for skill, count in job_skill_counts.items():
        strength = get_skill_strength(count)
        progress_value = min(count / 4, 1.0)

        st.write(skill.upper(), "-", strength)
        st.progress(progress_value)

    st.subheader("📘 Learning Roadmap")
    for skill in missing:
        if skill in learning_roadmap:
            st.markdown(f"**{skill.upper()}**")
            for step in learning_roadmap[skill]:
                st.write("•", step)
