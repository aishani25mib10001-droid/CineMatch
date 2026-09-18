# Problem Statement

Manually browsing a large movie catalogue to find something similar to
a film you enjoyed is time-consuming and relies on the platform's
often opaque, black-box recommendation logic. Many "recommendation
system" student projects tackle this with collaborative filtering,
which needs large volumes of user rating data that a solo project
cannot realistically collect. There is a need for a lightweight,
fully transparent, locally-runnable recommender that works from
content alone (what a movie *is about*) rather than from user
behaviour data.

# Scope of the Project

CineMatch is a command-line, content-based movie recommendation
system. Given a movie title, it returns the most similar movies from
a bundled catalogue, using classical machine learning techniques
(TF-IDF vectorization and cosine similarity) rather than collaborative
filtering or a pre-trained black-box model. The scope deliberately
excludes user accounts, rating collection, a graphical interface, and
online API calls — the project's purpose is to demonstrate a correct,
well-engineered application of a content-based ML technique end to
end, from raw data to an interactive result.

# Target Users

- Students and instructors evaluating the correct application of a
  classical ML technique (TF-IDF + cosine similarity) in a small,
  auditable codebase.
- Anyone who wants quick, offline movie suggestions based on a film
  they already like, without creating an account or sharing rating
  history with a third-party platform.

# High-Level Features

- Content-based recommendation: enter a movie title, receive the
  top-N most similar movies ranked by similarity score.
- Fuzzy title matching so minor typos or case differences still
  resolve to the correct movie.
- Dataset analytics command reporting genre distribution and
  catalogue statistics.
- Full catalogue listing command.
- Session logging for every load, vectorization, and recommendation
  event.
- Automated test suite validating the ML pipeline, error handling,
  and analytics output.
