from src.data_loader import load_movies, DataLoadError
from src.preprocessor import vectorize
from src.recommender import RecommendationEngine, MovieNotFoundError
from src.analytics import format_summary_report
from src.logger_config import get_logger

logger = get_logger(__name__)

BANNER = """
 ______________________________________
|            CineMatch v1.0             |
|  Content-Based Movie Recommender CLI  |
|________________________________________|

Commands:
  <movie title>   -> get recommendations similar to that movie
  list            -> show all movies in the catalogue
  stats           -> show dataset analytics
  quit / exit     -> leave CineMatch
"""


def run():
    try:
        df = load_movies()
    except DataLoadError as exc:
        print(f"[FATAL] Could not start CineMatch: {exc}")
        logger.error("Startup aborted: %s", exc)
        return

    vectorizer, matrix = vectorize(df)
    engine = RecommendationEngine(df, matrix)

    print(BANNER)
    print(f"Loaded {len(df)} movies. Type a movie title to begin.\n")

    while True:
        try:
            user_input = input("cinematch> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if user_input.lower() == "list":
            for title in df["title"].tolist():
                print(f"  - {title}")
            continue

        if user_input.lower() == "stats":
            print(format_summary_report(df))
            continue

        try:
            recs = engine.recommend(user_input)
            print(f"\nBecause you liked '{user_input}', you might enjoy:\n")
            for i, row in enumerate(recs.itertuples(), start=1):
                print(f"  {i}. {row.title}  "
                      f"[{row.genres}]  (similarity: {row.similarity})")
            print()
        except MovieNotFoundError as exc:
            print(f"  {exc}\n")


if __name__ == "__main__":
    run()
