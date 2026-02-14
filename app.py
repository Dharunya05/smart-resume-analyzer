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

SKILL_CATEGORIES = {
    "programming": [
        "python", "java", "c", "c++", "javascript"
    ],
    "data": [
        "sql", "machine learning", "data science",
        "artificial intelligence", "deep learning"
    ],
    "tools": [
        "power bi", "excel", "tableau", "canva"
    ],
    "cloud": [
        "aws", "azure", "gcp"
    ],
    "frameworks": [
        "react", "react native"
    ],
    "roles": [
        "business analyst", "data analyst", "software engineer"
    ]
}

STOPWORDS = {
    "resume", "project", "projects", "experience", "internship",
    "education", "year", "years", "months",
    "college", "university", "school",
    "skills", "tools", "technologies",
    "profile", "summary", "objective"
}

def extract_skills_dynamic(text):
    text = text.lower()
    found_skills = set()

    # Step 1: Flatten category skills
    category_skills = {}
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            category_skills[skill] = category

    # Step 2: Exact phrase matching (important for ML, Power BI etc.)
    for skill in category_skills:
        if skill in text:
            found_skills.add(skill)

    # Step 3: Section-based extraction (skills section)
    section_keywords = ["skills", "technologies", "tools", "expertise", "technical skills"]
    for keyword in section_keywords:
        if keyword in text:
            section_text = text.split(keyword, 1)[1][:300]
            for part in re.split(r",|\n|•|-", section_text):
                part = part.strip()
                if part in category_skills:
                    found_skills.add(part)

    categorized = {}
    for skill in found_skills:
        for category, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                categorized.setdefault(category, []).append(skill.upper())

    return categorized

def extract_uncategorized_skills(text, categorized_skills):
    """
    Detect skills that are not present in predefined categories
    """
    # All known skills (flatten)
    known_skills = set()
    for skills in SKILL_CATEGORIES.values():
        for s in skills:
            known_skills.add(s.lower())

    # Extract candidate words (capitalized / technical-looking)
    words = re.findall(r'\b[a-zA-Z][a-zA-Z+.#]{1,}\b', text)

    others = set()
    for word in words:
        w = word.lower()
        if (
            w not in known_skills and
            w not in STOPWORDS and
            len(w) > 1 and
            w not in categorized_skills
        ):
            others.add(w.upper())

    return sorted(others)

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

def default_roadmap(skill):
    return [
        f"Understand basics of {skill}",
        f"Learn core concepts and terminology",
        f"Practice hands-on exercises or mini projects",
        f"Explore real-world use cases of {skill}",
        f"Build at least one project using {skill}"
    ]

def learning_links(skill):
    skill_query = skill.replace(" ", "+")
    return {
        "YouTube": f"https://www.youtube.com/results?search_query={skill_query}+tutorial",
        "Coursera": f"https://www.coursera.org/search?query={skill_query}",
        "Google": f"https://www.google.com/search?q=learn+{skill_query}"
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
    resume_skills_by_category = extract_skills_dynamic(resume_text)
    resume_skills = [s for skills in resume_skills_by_category.values() for s in skills]

    uncategorized_skills = extract_uncategorized_skills(
        resume_text,
        [s.lower() for s in resume_skills]
    )

    skill_freq = skill_frequency(resume_text, resume_skills)
    progress.progress(60)

    if not resume_skills:
        st.warning("⚠️ No matching technical skills found in the resume.")

    # Step 3: Compare skills
    status.info("📊 Comparing with job description...")

    job_desc_clean = clean_text(job_desc)
    job_skills_by_category = extract_skills_dynamic(job_desc_clean)
    job_skills = [s for skills in job_skills_by_category.values() for s in skills]

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
    
    st.subheader("📦 Other Detected Skills (Uncategorized)")

    if uncategorized_skills:
        for skill in uncategorized_skills:
            st.write("•", skill)
    else:
        st.write("No uncategorized skills detected")

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
        st.markdown(f"### 🔹 {skill.upper()}")

        # Case 1: Curated roadmap exists
        if skill in learning_roadmap:
            for step in learning_roadmap[skill]:
                st.write("•", step)

        # Case 2: Default roadmap (fallback)
        else:
            steps = default_roadmap(skill)
            for step in steps:
                st.write("•", step)

            links = learning_links(skill)
            st.markdown(
                f"[🎥 YouTube]({links['YouTube']}) | "
                f"[🎓 Coursera]({links['Coursera']}) | "
                f"[🌐 Google]({links['Google']})"
            )

