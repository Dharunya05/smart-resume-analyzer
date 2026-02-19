📄 Smart Resume Analyzer & Skill Gap Detector

A Streamlit-based application that analyzes a resume against a job description to identify matched skills, missing skills, and learning recommendations.
This project is built mainly for learning and resume improvement purposes.

🎯 Objective

1) Extract skills from resumes (text-based and scanned PDFs)

2) Compare resume skills with a job description

3) Calculate a resume–JD match percentage

4) Identify missing skills and suggest learning roadmaps

🚀 Features

Supports text-based and image-based PDF resumes (OCR)

Category-based skill extraction

Skill normalization (e.g., ML → Machine Learning)

Skill frequency and strength analysis

Matched & missing skill detection

Learning roadmap with useful links

🧠 Completed Levels

Level 1 – Resume Text Extraction

PDF text extraction using pdfplumber

OCR fallback using pytesseract for scanned resumes

Level 2 – Skill Extraction

Predefined skill categories

Exact phrase matching

Section-aware skill detection

Level 3 – Skill Analysis

Skill normalization & synonyms

Resume–JD comparison

Match score calculation

Skill gap explanation and roadmap generation


🛠️ Tech Stack

1) Python

2) Streamlit

3) pdfplumber

4) pytesseract

5) pdf2image

6) Regular Expressions


⚠️ Known Limitation

Skill frequency is based on word-boundary matching

Advanced contextual NLP is not implemented (intentional for learning stage)

▶️ How to Run

pip install streamlit pdfplumber pytesseract pdf2image
streamlit run app.py

📌 Conclusion

This project demonstrates a complete resume analysis pipeline with clear logic, honest limitations, and learning-focused design.
It is suitable for academic projects and portfolio use.
