
import pandas as pd
from collections import Counter

from src.logger_config import get_logger

logger = get_logger(__name__)


def genre_distribution(df: pd.DataFrame) -> pd.Series:
    """Count how many movies fall under each individual genre tag."""
    all_genres = df["genres"].str.split().explode()
    counts = Counter(all_genres)
    series = pd.Series(counts).sort_values(ascending=False)
    return series


def dataset_summary(df: pd.DataFrame) -> dict:
    """Return a small dict of headline stats about the loaded catalogue."""
    dist = genre_distribution(df)
    summary = {
        "total_movies": len(df),
        "unique_genre_tags": len(dist),
        "most_common_genre": dist.index[0] if not dist.empty else "N/A",
        "most_common_genre_count": int(dist.iloc[0]) if not dist.empty else 0,
    }
    logger.info("Computed dataset summary: %s", summary)
    return summary


def format_summary_report(df: pd.DataFrame) -> str:
    """Human-readable analytics block printed by the CLI's 'stats' command."""
    summary = dataset_summary(df)
    dist = genre_distribution(df).head(8)

    lines = [
        "=" * 46,
        " CineMatch Dataset Analytics",
        "=" * 46,
        f"Total movies in catalogue : {summary['total_movies']}",
        f"Distinct genre tags       : {summary['unique_genre_tags']}",
        f"Most common genre         : {summary['most_common_genre']} "
        f"({summary['most_common_genre_count']} movies)",
        "-" * 46,
        "Top genres:",
    ]
    for genre, count in dist.items():
        lines.append(f"  {genre:<15} {count}")
    lines.append("=" * 46)
    return "\n".join(lines)
