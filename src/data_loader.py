"""
data_loader.py
---------------
Functional Module 1: Data Ingestion & Preprocessing (part A)

Responsible only for reading the raw movie catalogue off disk and
validating that it has the shape the rest of the system expects.
Keeping I/O separate from cleaning/vectorization (preprocessor.py)
keeps each file single-purpose -> Maintainability.
"""

import os
import pandas as pd

from src.config import DATA_PATH
from src.logger_config import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = {"movie_id", "title", "genres", "overview"}


class DataLoadError(Exception):
    """Raised when the movie dataset cannot be loaded or is malformed."""


def load_movies(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the movie catalogue CSV into a DataFrame.

    Raises
    ------
    DataLoadError
        If the file is missing, empty, or missing required columns.
        Surfacing a clear custom exception (rather than letting a raw
        pandas/OS error bubble up) is part of the Reliability /
        error-handling requirement.
    """
    if not os.path.exists(path):
        logger.error("Dataset not found at %s", path)
        raise DataLoadError(f"Dataset file not found: {path}")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        logger.error("Dataset at %s is empty", path)
        raise DataLoadError(f"Dataset file is empty: {path}") from exc
    except pd.errors.ParserError as exc:
        logger.error("Dataset at %s is malformed: %s", path, exc)
        raise DataLoadError(f"Could not parse dataset: {exc}") from exc

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        logger.error("Dataset missing required columns: %s", missing)
        raise DataLoadError(f"Dataset missing required columns: {missing}")

    if df.empty:
        logger.error("Dataset loaded but contains zero rows")
        raise DataLoadError("Dataset contains no movies")

    df = df.dropna(subset=["title", "genres"]).reset_index(drop=True)
    logger.info("Loaded %d movies from %s", len(df), path)
    return df
