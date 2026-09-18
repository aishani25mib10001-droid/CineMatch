import difflib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.config import DEFAULT_TOP_N
from src.logger_config import get_logger

logger = get_logger(__name__)


class MovieNotFoundError(Exception):
    """Raised when a requested movie title cannot be matched in the dataset."""


class RecommendationEngine:
    """
    Wraps the fitted TF-IDF matrix and exposes a simple
    `recommend(title)` API. The similarity matrix is computed once
    at construction time and cached -- repeated recommendations are
    then just an O(1) row lookup, which is what gives the system its
    Performance characteristic for a catalogue of this size.
    """

    def __init__(self, df: pd.DataFrame, tfidf_matrix):
        self.df = df.reset_index(drop=True)
        self.titles = self.df["title"].tolist()
        self._title_to_index = {
            title.lower(): idx for idx, title in enumerate(self.titles)
        }
        logger.info("Computing cosine similarity matrix (%d x %d)...",
                    len(self.titles), len(self.titles))
        self.similarity_matrix = cosine_similarity(tfidf_matrix)

    def _resolve_title(self, query: str) -> int:
        """
        Match a user-typed title to a dataset row, tolerating case
        differences and minor typos (fuzzy matching). Raises
        MovieNotFoundError with a helpful suggestion list on failure
        -- part of the Usability / error-handling requirements.
        """
        query_lower = query.strip().lower()

        if query_lower in self._title_to_index:
            return self._title_to_index[query_lower]

        close = difflib.get_close_matches(
            query_lower, self._title_to_index.keys(), n=3, cutoff=0.5
        )
        if close:
            best = close[0]
            logger.info("Fuzzy-matched '%s' -> '%s'", query, best)
            return self._title_to_index[best]

        logger.warning("No match found for query '%s'", query)
        raise MovieNotFoundError(
            f"No movie found matching '{query}'. "
            f"Try one of: {', '.join(self.titles[:5])} ..."
        )

    def recommend(self, title: str, top_n: int = DEFAULT_TOP_N) -> pd.DataFrame:
        """
        Return the top_n movies most similar to `title`.

        Raises
        ------
        MovieNotFoundError
            If the title cannot be matched, even fuzzily.
        """
        idx = self._resolve_title(title)
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = [s for s in scores if s[0] != idx]  # exclude itself
        scores.sort(key=lambda x: x[1], reverse=True)
        top = scores[:top_n]

        result = self.df.iloc[[i for i, _ in top]].copy()
        result["similarity"] = [round(score, 3) for _, score in top]
        logger.info("Generated %d recommendations for '%s'", len(result), title)
        return result[["title", "genres", "similarity"]]
