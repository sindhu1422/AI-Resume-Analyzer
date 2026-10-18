
# AI Resume Analyzer

A Python-based web application that compares a resume
with a job description and identifies matching skills
and missing keywords.

## Features
- Upload a resume in PDF format
- Extract text from the resume
- Identify recognized skills
- Compare skills with a job description
- Display an estimated keyword match percentage

## Technologies
- Python
- Streamlit
- pypdf
- Regular Expressions

## Installation

Install the dependencies:

    python -m pip install streamlit pypdf

## Run the application

    python -m streamlit run app.py

## How it works

The application extracts text from a PDF and uses
keyword matching to compare resume skills with the
requirements in a job description.

The match percentage is a keyword-based estimate,
not a prediction of hiring success.
