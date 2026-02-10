📄 Smart Resume Analyzer & Skill Gap Detector

A Streamlit-based web application that analyzes a user’s resume against a job description to extract skills, calculate match percentage, identify skill gaps, and provide a learning roadmap.

🔗 Live App: https://smart-resume-analyzer-rq4h2lyjrfxaieqzyn4tc6.streamlit.app/~/+/#what-this-app-does


🚀 Features

✅ Resume Skill Extraction:

Extracts technical skills from text-based PDF resumes

Supports skills like Python, SQL, Power BI, Excel, ML, Data Science, AI, Statistics

✅ Job Description Skill Analysis:

Extracts required skills directly from the Job Description

Compares resume skills with JD skills dynamically

✅ Resume–Job Match Score:

Calculates match percentage based on matched skills

Helps users understand their suitability for a role

✅ Skill Gap Detection:


Clearly shows:

🟢 Matched Skills

🔴 Missing Skills


✅ Skill Strength Analysis:

Measures how strongly each skill appears in the resume

Categorizes skills as High / Medium / Low based on frequency

✅ Skill Coverage Visualization:

Visual progress bars showing:

How much each JD skill is covered in the job description

Relative importance of skills in the JD

✅ Learning Roadmap:

Provides step-by-step learning guidance for missing skills

Helps users plan upskilling effectively

🛠️ Tech Stack:

Python

Streamlit

pdfplumber

Regular Expressions (Regex)

GitHub

Streamlit Community Cloud

📌 How It Works:

Upload a text-based PDF resume

Paste the Job Description

App performs:

Resume text extraction

Skill identification

Skill matching & gap analysis

Match score calculation

Skill strength & coverage analysis

Results and learning roadmap are displayed instantly


⚠️ Limitations:

Supports only text-based PDFs (scanned/image resumes not supported yet)

Skill extraction is currently rule-based

AI/NLP-based extraction planned in future versions


🔮 Future Enhancements:

AI-powered skill extraction using NLP

Support for synonyms (e.g., ML ↔ Machine Learning)

Scanned resume (OCR) support

Resume improvement suggestions

Role-based skill weighting


⭐ If you like this project:

Give it a ⭐ on GitHub — it motivates further improvements!
