print("RUNNING FILE:", __file__)

import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
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

    found_skills = []
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills

def skill_gap_analysis(resume_skills, job_skills):
    resume_set = set(skill.lower().strip() for skill in resume_skills)
    job_set = set(skill.lower().strip() for skill in job_skills)

    matched = sorted(resume_set.intersection(job_set))
    missing = sorted(job_set - resume_set)

    return matched, missing

def calculate_match_score(matched_skills, total_job_skills):
    if total_job_skills == 0:
        return 0
    score = (len(matched_skills) / total_job_skills) * 100
    return round(score, 2)

learning_roadmap = {
    "deep learning": [
        "Neural Networks basics",
        "Activation functions",
        "CNN and RNN",
        "PyTorch or TensorFlow projects"
    ],
    "statistics": [
        "Descriptive statistics",
        "Probability theory",
        "Hypothesis testing",
        "Regression analysis"
    ],
    "tableau": [
        "Basic charts and filters",
        "Dashboards and storytelling",
        "Connecting Tableau with datasets",
        "Mini visualization projects"
    ],
    "sql": [
        "Joins and subqueries",
        "Window functions",
        "Query optimization",
        "SQL case study projects"
    ]
}

def generate_learning_plan(missing_skills):
    print("\n===== LEARNING ROADMAP =====")
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in learning_roadmap:
            print(f"\n📌 {skill.upper()}")
            for step in learning_roadmap[skill_lower]:
                print("  -", step)
        else:
            print(f"\n📌 {skill.upper()}")
            print("  - Learn fundamentals and practice with projects")

# ---------- MAIN ----------
pdf_path = "sample_resume.pdf"

raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
skills = extract_skills(cleaned_text)

print("\n===== EXTRACTED SKILLS =====")
for skill in skills:
    print("-", skill)

job_required_skills = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tableau",
    "statistics"
]

matched_skills, missing_skills = skill_gap_analysis(skills, job_required_skills)

print("\n===== SKILL GAP ANALYSIS =====")
print("Matched Skills:")
for skill in matched_skills:
    print("✔", skill.upper())

print("\nMissing Skills:")
for skill in missing_skills:
    print("✖", skill.upper())

match_score = calculate_match_score(
    matched_skills,
    len(job_required_skills)
)

print("\n===== RESUME MATCH SCORE =====")
print(f"Resume matches {match_score}% of the job requirements")

generate_learning_plan(missing_skills)
