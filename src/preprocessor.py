"""
preprocessor.py
----------------
Functional Module 1: Data Ingestion & Preprocessing (part B)

Turns the raw text columns (genres + overview) into a single
"content soup" per movie, then vectorizes that text with TF-IDF.
This produces the numeric feature matrix that the ML core
(recommender.py) needs -- this is where "AI/ML" actually enters
the pipeline.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from src.config import TFIDF_STOP_WORDS
from src.logger_config import get_logger

logger = get_logger(__name__)


def build_content_soup(df: pd.DataFrame) -> pd.Series:
    """
    Combine genres and overview into one text field per movie.
    Genres are repeated 3x so they weigh more heavily than the
    free-text overview when vectorized -- a deliberate, documented
    design choice (see report: Design Decisions & Rationale).
    """
    soup = (df["genres"].fillna("") + " ") * 3 + df["overview"].fillna("")
    return soup.str.lower()


def vectorize(df: pd.DataFrame):
    """
    Fit a TF-IDF vectorizer on the content soup and return both the
    fitted vectorizer and the resulting sparse feature matrix.

    Returns
    -------
    (TfidfVectorizer, scipy.sparse matrix)
    """
    soup = build_content_soup(df)
    vectorizer = TfidfVectorizer(stop_words=TFIDF_STOP_WORDS)
    matrix = vectorizer.fit_transform(soup)
    logger.info(
        "Vectorized %d movies into a %d-term TF-IDF matrix",
        matrix.shape[0],
        matrix.shape[1],
    )
    return vectorizer, matrix
