
import re
import streamlit as st
from pypdf import PdfReader

# Skills the analyzer knows how to recognize
SKILLS = [
    "python", "java", "c++", "sql", "mysql", "postgresql",
    "mongodb", "pandas", "numpy", "scikit-learn",
    "machine learning", "deep learning", "generative ai",
    "natural language processing", "nlp", "data analysis",
    "data engineering", "data visualization", "statistics",
    "power bi", "tableau", "excel", "etl", "airflow",
    "apache spark", "aws", "azure", "git", "github",
    "docker", "linux", "streamlit", "flask", "django",
    "html", "css", "javascript", "react", "api",
    "communication", "problem solving"
]


def extract_resume_text(pdf_file):
    """Read text from an uploaded PDF."""
    reader = PdfReader(pdf_file)
    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    return "\n".join(pages)


def find_skills(text):
    """Find recognized skills using keyword matching."""
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


# Web app interface
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and compare it with a job description."
)

st.info(
    "Free demo: uses keyword matching, not a trained AI model. "
    "The match score is an estimate, not a hiring prediction."
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Paste the responsibilities and required skills..."
)

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload a PDF resume.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        try:
            resume_text = extract_resume_text(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "No readable text found. Try a text-based PDF "
                    "instead of a scanned image."
                )

            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                matched = [
                    skill for skill in job_skills
                    if skill in resume_skills
                ]

                missing = [
                    skill for skill in job_skills
                    if skill not in resume_skills
                ]

                st.subheader("Analysis Results")

                if not job_skills:
                    st.warning(
                        "No supported skills were recognized in "
                        "the job description. Try including specific "
                        "technical skills."
                    )

                else:
                    score = round(
                        len(matched) / len(job_skills) * 100
                    )

                    st.metric(
                        "Estimated keyword match",
                        f"{score}%"
                    )

                    st.progress(score / 100)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.success(
                            f"Matched skills: {len(matched)}"
                        )
                        if matched:
                            st.write(", ".join(matched))
                        else:
                            st.write("No matching skills found.")

                    with col2:
                        st.warning(
                            f"Missing keywords: {len(missing)}"
                        )
                        if missing:
                            st.write(", ".join(missing))
                        else:
                            st.write("No recognized keywords missing.")

                    st.subheader("Skills Found in Your Resume")
                    if resume_skills:
                        st.write(", ".join(resume_skills))
                    else:
                        st.write(
                            "No supported skills were recognized."
                        )

                    st.caption(
                        "This score measures recognized keywords "
                        "only. It does not assess experience, skill "
                        "proficiency, or overall candidate suitability."
                    )

        except Exception as error:
            st.error(
                "Could not read this PDF. Please try another "
                "text-based PDF. Details: " + str(error)
            )
