"""
resumegap_engine.py
====================
LOCKED — Day 198 finalized core engine for ResumeGapAI.
This file is the "Raw Data" layer for Day 199. Do NOT modify it during
Day 199 practice tasks. Day 199 work happens in app.py, README.md,
requirements.txt, and deployment config only.

Functions (as corrected in Day198's second resubmission, scored 100/100):
    clean_text(text)                         -> str
    tfidf_similarity_naive(resume, jd)       -> float (0-100)
    tfidf_similarity_fixed(resume, jd)       -> float (0-100)
    gap_words(resume, jd, top_n=8)           -> list[str]
    analyze_resume_gap(resume, jd)           -> dict
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

# Background corpus fixes the 2-document IDF collapse problem (Day198 lesson).
# Fitting TF-IDF on ONLY resume+JD gives every term near-identical IDF,
# because IDF = log(N_docs / docs_containing_term) collapses when N_docs=2.
BACKGROUND_CORPUS = [
    "experienced data analyst skilled in sql python and excel reporting",
    "data scientist with expertise in machine learning and statistical modeling",
    "software engineer proficient in python java and cloud infrastructure aws gcp",
    "project manager coordinating cross functional teams and agile delivery",
    "marketing specialist focused on digital campaigns and content strategy",
    "financial analyst experienced in forecasting budgeting and excel modeling",
    "product manager driving roadmap strategy and stakeholder alignment",
    "business analyst gathering requirements and documenting processes",
    "machine learning engineer building and deploying production models",
    "data engineer building etl pipelines and managing data warehouses",
]


def clean_text(text: str) -> str:
    """
    Lowercase and strip punctuation/special characters.
    CRITICAL: replacement must be a SPACE, not empty string — otherwise
    'AWS/GCP' collapses into 'awsgcp' and destroys gap-word extraction.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # space, not '' — Day198 bugfix
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tfidf_similarity_naive(resume: str, jd: str) -> float:
    """Fits TF-IDF on ONLY the resume+JD pair. Demonstrates the IDF-collapse bug."""
    docs = [clean_text(resume), clean_text(jd)]
    vec = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
    matrix = vec.fit_transform(docs)
    sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(sim * 100, 2)


def tfidf_similarity_fixed(resume: str, jd: str) -> float:
    """Fits TF-IDF on background corpus + pair, scores only the pair. The real fix."""
    docs = BACKGROUND_CORPUS + [clean_text(resume), clean_text(jd)]
    vec = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
    matrix = vec.fit_transform(docs)
    resume_vec = matrix[-2:-1]
    jd_vec = matrix[-1:]
    sim = cosine_similarity(resume_vec, jd_vec)[0][0]
    return round(sim * 100, 2)


def gap_words(resume: str, jd: str, top_n: int = 8) -> list:
    """Words present in the JD (high TF-IDF weight) but absent from the resume."""
    resume_clean = clean_text(resume)
    jd_clean = clean_text(jd)
    docs = BACKGROUND_CORPUS + [resume_clean, jd_clean]
    vec = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
    matrix = vec.fit_transform(docs)
    feature_names = vec.get_feature_names_out()

    jd_vector = matrix[-1].toarray()[0]
    resume_words = set(resume_clean.split())

    scored = [
        (feature_names[i], jd_vector[i])
        for i in range(len(feature_names))
        if jd_vector[i] > 0 and feature_names[i] not in resume_words
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _score in scored[:top_n]]


def analyze_resume_gap(resume: str, jd: str) -> dict:
    """Single wrapper the Streamlit UI calls. Returns everything the UI needs."""
    return {
        "similarity_naive": tfidf_similarity_naive(resume, jd),
        "similarity_fixed": tfidf_similarity_fixed(resume, jd),
        "gap_words": gap_words(resume, jd, top_n=8),
    }
