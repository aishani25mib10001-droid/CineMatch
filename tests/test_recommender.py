"""
test_recommender.py
--------------------
Validation tests covering the ML core (recommender.py), the
preprocessing pipeline, and the analytics module. Run with:

    python -m pytest tests/ -v
"""

import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_movies, DataLoadError
from src.preprocessor import vectorize, build_content_soup
from src.recommender import RecommendationEngine, MovieNotFoundError
from src.analytics import dataset_summary, genre_distribution


@pytest.fixture(scope="module")
def movies_df():
    return load_movies()


@pytest.fixture(scope="module")
def engine(movies_df):
    _, matrix = vectorize(movies_df)
    return RecommendationEngine(movies_df, matrix)


def test_dataset_loads_with_required_columns(movies_df):
    assert {"title", "genres", "overview"}.issubset(movies_df.columns)
    assert len(movies_df) > 0


def test_missing_dataset_raises_error():
    with pytest.raises(DataLoadError):
        load_movies(path="data/does_not_exist.csv")


def test_content_soup_is_lowercase(movies_df):
    soup = build_content_soup(movies_df)
    assert soup.iloc[0] == soup.iloc[0].lower()


def test_recommend_returns_requested_count(engine):
    recs = engine.recommend("Inception", top_n=5)
    assert len(recs) == 5
    assert "Inception" not in recs["title"].tolist()  # never recommend itself


def test_recommend_is_thematically_sensible(engine):
    # Interstellar is a sci-fi/drama movie; at least one of its top
    # recommendations should share the sci-fi tag.
    recs = engine.recommend("Interstellar", top_n=5)
    assert any("Sci-Fi" in g for g in recs["genres"])


def test_fuzzy_matching_tolerates_typos(engine):
    recs = engine.recommend("intersteller")  # deliberate typo
    assert len(recs) > 0


def test_unknown_movie_raises_custom_error(engine):
    with pytest.raises(MovieNotFoundError):
        engine.recommend("ThisMovieDoesNotExist12345")


def test_genre_distribution_counts_correctly(movies_df):
    dist = genre_distribution(movies_df)
    assert dist.sum() >= len(movies_df)  # each movie has >=1 genre tag
    assert "Drama" in dist.index


def test_dataset_summary_shape(movies_df):
    summary = dataset_summary(movies_df)
    assert set(summary.keys()) == {
        "total_movies", "unique_genre_tags",
        "most_common_genre", "most_common_genre_count",
    }
    assert summary["total_movies"] == len(movies_df)
