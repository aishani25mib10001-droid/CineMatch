"""
build_report.py
----------------
Generates the project report PDF (CineMatch_Project_Report.pdf)
required by the submission guidelines, using reportlab.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, ListFlowable, ListItem, KeepTogether
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontSize=26, leading=32,
                           alignment=TA_CENTER, spaceAfter=14, textColor=colors.HexColor("#1f3864")))
styles.add(ParagraphStyle(name="CoverSub", fontSize=14, leading=20,
                           alignment=TA_CENTER, textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"],
                           textColor=colors.HexColor("#1f3864"), spaceBefore=16))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"],
                           textColor=colors.HexColor("#2E5395"), spaceBefore=10))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"],
                           fontSize=10.3, leading=15, spaceAfter=8))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"],
                           fontSize=8.5, leading=11, alignment=TA_CENTER,
                           textColor=colors.HexColor("#555555"), spaceAfter=14))

story = []

# ---------------- COVER PAGE ----------------
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("CineMatch", styles["CoverTitle"]))
story.append(Paragraph("A Content-Based Movie Recommendation System", styles["CoverSub"]))
story.append(Spacer(1, 1.5 * cm))
story.append(Paragraph("Project Report — VITyarthi \"Build Your Own Project\"", styles["CoverSub"]))
story.append(Paragraph("Course Domain: AI / Machine Learning", styles["CoverSub"]))
story.append(Spacer(1, 3 * cm))
cover_cell = ParagraphStyle(name="CoverCell", parent=styles["Normal"], fontSize=10.5, leading=14)
cover_label = ParagraphStyle(name="CoverLabel", parent=styles["Normal"], fontSize=10.5,
                              leading=14, fontName="Helvetica-Bold")
cover_table = Table([
    [Paragraph("Submitted by:", cover_label), Paragraph("FROST", cover_cell)],
    [Paragraph("Repository:", cover_label),
     Paragraph("https://github.com/{github-username}/{repo-name}", cover_cell)],
    [Paragraph("Technique used:", cover_label),
     Paragraph("TF-IDF Vectorization + Cosine Similarity", cover_cell)],
], colWidths=[4 * cm, 10 * cm])
cover_table.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(cover_table)
story.append(PageBreak())

# ---------------- 1. INTRODUCTION ----------------
story.append(Paragraph("1. Introduction", styles["H1"]))
story.append(Paragraph(
    "CineMatch is a command-line AI/ML application that recommends movies similar to "
    "one a user already likes. It demonstrates a complete, correctly-engineered "
    "content-based filtering pipeline: raw text data (genres and plot overviews) is "
    "converted into numeric TF-IDF vectors, and recommendations are produced by "
    "finding the nearest neighbours of a chosen movie in that vector space using "
    "cosine similarity. The project favours a small, fully offline, easily auditable "
    "implementation over a large dataset or an external API, so that every stage of "
    "the ML pipeline is visible and testable within the codebase itself.",
    styles["Body"]))

# ---------------- 2. PROBLEM STATEMENT ----------------
story.append(Paragraph("2. Problem Statement", styles["H1"]))
story.append(Paragraph(
    "Manually browsing a large movie catalogue to find something similar to a film "
    "already enjoyed is time-consuming and depends on a platform's opaque, black-box "
    "recommendation logic. Many student projects address recommendation with "
    "collaborative filtering, which requires large volumes of real user-rating data "
    "that a solo academic project cannot realistically collect. CineMatch instead "
    "solves this with a lightweight, transparent, locally-runnable recommender that "
    "works purely from movie content -- genre tags and plot text -- rather than from "
    "user behaviour data.",
    styles["Body"]))

# ---------------- 3. FUNCTIONAL REQUIREMENTS ----------------
story.append(Paragraph("3. Functional Requirements", styles["H1"]))
func_reqs = [
    "<b>Module 1 -- Data Ingestion &amp; Preprocessing:</b> load the movie catalogue "
    "from CSV, validate its structure, combine genre and overview text per movie, "
    "and vectorize it with TF-IDF.",
    "<b>Module 2 -- Recommendation Engine (ML core):</b> compute a cosine-similarity "
    "matrix over the TF-IDF vectors and, given a movie title, return the top-N most "
    "similar movies with their similarity scores.",
    "<b>Module 3 -- CLI &amp; Analytics:</b> an interactive command-line interface that "
    "accepts a movie title, a 'list' command, and a 'stats' command that reports "
    "genre-distribution analytics over the loaded catalogue.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in func_reqs],
    bulletType="bullet"))
story.append(Paragraph(
    "<b>Input/Output structure:</b> input is a free-text movie title typed at the "
    "prompt; output is a ranked table of recommended titles, genres, and similarity "
    "scores (0-1). <b>Workflow:</b> Load dataset &rarr; preprocess &amp; vectorize &rarr; "
    "compute similarity matrix once &rarr; repeatedly accept user commands until the "
    "user exits.", styles["Body"]))

# ---------------- 4. NON-FUNCTIONAL REQUIREMENTS ----------------
story.append(Paragraph("4. Non-Functional Requirements", styles["H1"]))
nfr_data = [
    ["Requirement", "How CineMatch addresses it"],
    ["Performance", "Cosine-similarity matrix computed once at startup and cached; "
                     "each recommendation is an O(1) row lookup thereafter."],
    ["Usability", "Guided CLI prompts and fuzzy title matching tolerate typos and "
                   "case differences."],
    ["Reliability", "Custom exceptions (DataLoadError, MovieNotFoundError) replace "
                     "raw stack traces with actionable, user-facing messages."],
    ["Maintainability", "Each pipeline stage lives in its own single-purpose module "
                         "(ingest / preprocess / recommend / report / interact)."],
    ["Scalability", "Swapping data/movies.csv for a larger catalogue needs no code "
                     "changes, only a config.py path update."],
    ["Logging / Monitoring", "All key events (dataset load, vectorization, "
                              "recommendation requests, errors) are logged to "
                              "cinematch.log with timestamps."],
]
cell_style = ParagraphStyle(name="Cell", parent=styles["Normal"], fontSize=9, leading=12)
header_style = ParagraphStyle(name="CellHead", parent=styles["Normal"], fontSize=9,
                               leading=12, textColor=colors.white, fontName="Helvetica-Bold")
nfr_table_data = [[Paragraph(nfr_data[0][0], header_style), Paragraph(nfr_data[0][1], header_style)]]
for row in nfr_data[1:]:
    nfr_table_data.append([Paragraph(row[0], cell_style), Paragraph(row[1], cell_style)])

t = Table(nfr_table_data, colWidths=[3.6 * cm, 11.4 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3864")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FB")]),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(PageBreak())

# ---------------- 5. SYSTEM ARCHITECTURE ----------------
story.append(Paragraph("5. System Architecture", styles["H1"]))
story.append(Paragraph(
    "The system is organised into clearly separated layers: data access "
    "(data_loader.py), preprocessing/ML feature engineering (preprocessor.py), the "
    "ML core (recommender.py), presentation/reporting (cli.py, analytics.py), and "
    "cross-cutting concerns (config.py, logger_config.py). Each arrow below "
    "represents a function call and the data passed along with it.", styles["Body"]))
story.append(KeepTogether([
    Image("architecture_diagram.png", width=15.5 * cm, height=15.5 * cm * 640 / 960),
    Paragraph("Figure 1: System Architecture Diagram", styles["Caption"]),
]))

# ---------------- 6. DESIGN DIAGRAMS ----------------
story.append(Paragraph("6. Design Diagrams", styles["H1"]))

story.append(Paragraph("6.1 Use Case Diagram", styles["H2"]))
story.append(KeepTogether([
    Image("use_case_diagram.png", width=14 * cm, height=14 * cm * 900 / 1200),
    Paragraph("Figure 2: Use Case Diagram", styles["Caption"]),
]))

story.append(Paragraph("6.2 Process Flow / Workflow Diagram", styles["H2"]))
story.append(KeepTogether([
    Image("workflow_diagram.png", width=9 * cm, height=9 * cm * 1300 / 864),
    Paragraph("Figure 3: Workflow Diagram", styles["Caption"]),
]))

story.append(PageBreak())
story.append(Paragraph("6.3 Class / Component Diagram", styles["H2"]))
story.append(KeepTogether([
    Image("class_diagram.png", width=15.5 * cm, height=15.5 * cm * 800 / 1500),
    Paragraph("Figure 4: Simplified UML Class / Component Diagram", styles["Caption"]),
]))

story.append(Paragraph("6.4 Sequence Diagram", styles["H2"]))
story.append(KeepTogether([
    Image("sequence_diagram.png", width=15.5 * cm, height=15.5 * cm * 700 / 1350),
    Paragraph("Figure 5: Sequence Diagram -- 'Get Recommendations' happy path", styles["Caption"]),
]))

story.append(Paragraph(
    "<b>Note on storage/ER diagrams:</b> CineMatch reads a static bundled CSV file "
    "and holds all data in memory (pandas DataFrame) for the duration of a session; "
    "there is no database or persistent storage layer, so an ER diagram / schema "
    "design is not applicable to this project.", styles["Body"]))

if False:
    pass  # dataset/model rationale is combination-heavy course requirement, handled in section 7 below
story.append(PageBreak())

# ---------------- 7. DESIGN DECISIONS & RATIONALE ----------------
story.append(Paragraph("7. Design Decisions &amp; Rationale", styles["H1"]))
decisions = [
    "<b>Content-based filtering over collaborative filtering:</b> collaborative "
    "filtering needs a large user-item rating matrix that does not exist for a "
    "solo project; content-based filtering only needs item metadata, which can be "
    "curated directly.",
    "<b>TF-IDF over simple keyword matching:</b> TF-IDF down-weights common words "
    "(e.g. 'the', 'man') and up-weights terms that are distinctive to a particular "
    "movie's description, giving more meaningful similarity scores than raw "
    "keyword overlap.",
    "<b>Genre text repeated 3x in the 'content soup':</b> genre tags are a stronger, "
    "cleaner similarity signal than free-text overviews, so they are deliberately "
    "weighted more heavily before vectorization (see preprocessor.py).",
    "<b>Cosine similarity over Euclidean distance:</b> cosine similarity is "
    "invariant to document length, which matters here because overview lengths "
    "vary considerably across movies while genre-tag counts do not.",
    "<b>Similarity matrix pre-computed once at startup:</b> trades a small amount "
    "of startup time for O(1) lookups during the interactive session, which is "
    "the right trade-off for a tool used interactively and repeatedly.",
    "<b>Dataset description:</b> a hand-curated 40-movie catalogue spanning 16 "
    "genre tags was used instead of a very large public dataset, so the whole "
    "pipeline runs instantly with no download step and every recommendation "
    "can be manually sanity-checked against the source data.",
    "<b>Model selection rationale:</b> TF-IDF + cosine similarity was chosen over "
    "a pre-trained embedding model (e.g. sentence-transformers) because it needs "
    "no external model download, runs deterministically offline, and is simple "
    "enough to explain and defend line-by-line -- appropriate for a course project "
    "whose goal is demonstrating understanding of the underlying ML technique.",
    "<b>Evaluation methodology:</b> correctness was checked two ways -- (a) automated "
    "unit tests asserting that recommended movies share genre tags with the query "
    "movie and that a movie never recommends itself, and (b) manual inspection "
    "confirming that, e.g., querying a science-fiction film returns other "
    "science-fiction films as its top matches (see Section 10, Screenshots).",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in decisions],
    bulletType="bullet"))

# ---------------- 8. IMPLEMENTATION DETAILS ----------------
story.append(Paragraph("8. Implementation Details", styles["H1"]))
story.append(Paragraph(
    "The project is implemented in Python 3 using pandas for data handling and "
    "scikit-learn for the ML pipeline (TfidfVectorizer, cosine_similarity). The "
    "codebase is split into 9 files across a src/ package, each with a single "
    "responsibility (see Section 6.3). Configuration (dataset path, default "
    "recommendation count) is centralised in config.py so behaviour can be tuned "
    "without touching logic files. All significant runtime events are written to "
    "a rotating text log (cinematch.log) via a shared logger factory in "
    "logger_config.py, satisfying the Logging / Monitoring requirement. User-facing "
    "errors are raised as custom exception types (DataLoadError, MovieNotFoundError) "
    "and caught at the CLI boundary so the terminal never shows a raw Python "
    "traceback to the end user.", styles["Body"]))
story.append(Paragraph(
    "Key modules and file count (satisfies the 5-10 meaningful "
    "modules/files requirement):", styles["Body"]))
files_list = [
    "main.py -- entry point",
    "src/config.py -- configuration",
    "src/logger_config.py -- shared logger",
    "src/data_loader.py -- dataset ingestion &amp; validation",
    "src/preprocessor.py -- TF-IDF feature engineering",
    "src/recommender.py -- ML recommendation engine",
    "src/analytics.py -- dataset analytics/reporting",
    "src/cli.py -- interactive command-line interface",
    "tests/test_recommender.py -- automated test suite",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in files_list],
    bulletType="bullet"))

story.append(Paragraph("9. Screenshots / Results", styles["H1"]))
story.append(Paragraph(
    "Below is a captured terminal session showing a recommendation query for "
    "'Interstellar' (a science-fiction/drama film) followed by the 'stats' "
    "analytics command. Note that all five returned recommendations are "
    "science-fiction and/or adventure titles, confirming the recommender is "
    "picking up on genuine thematic similarity rather than noise.", styles["Body"]))
story.append(Image("terminal_screenshot.png", width=14.5 * cm,
                    height=14.5 * cm * 1338 / 1013))
story.append(Paragraph("Figure 6: Live terminal session", styles["Caption"]))


# ---------------- 10. TESTING APPROACH ----------------
story.append(Paragraph("10. Testing Approach", styles["H1"]))
story.append(Paragraph(
    "An automated pytest suite (tests/test_recommender.py) covers the full "
    "pipeline with 9 tests: dataset structure/validity, correct error raising on "
    "a missing dataset file, correctness of the text-preprocessing step, correct "
    "recommendation count and self-exclusion, thematic sensibility of "
    "recommendations (genre overlap), fuzzy-matching tolerance for typos, correct "
    "exception raising for an unknown title, and correctness of the analytics "
    "summary. All 9 tests pass:", styles["Body"]))
story.append(Paragraph(
    "<font face='Courier'>============================= test session starts "
    "==============================<br/>"
    "collected 9 items<br/><br/>"
    "tests/test_recommender.py::test_dataset_loads_with_required_columns PASSED<br/>"
    "tests/test_recommender.py::test_missing_dataset_raises_error PASSED<br/>"
    "tests/test_recommender.py::test_content_soup_is_lowercase PASSED<br/>"
    "tests/test_recommender.py::test_recommend_returns_requested_count PASSED<br/>"
    "tests/test_recommender.py::test_recommend_is_thematically_sensible PASSED<br/>"
    "tests/test_recommender.py::test_fuzzy_matching_tolerates_typos PASSED<br/>"
    "tests/test_recommender.py::test_unknown_movie_raises_custom_error PASSED<br/>"
    "tests/test_recommender.py::test_genre_distribution_counts_correctly PASSED<br/>"
    "tests/test_recommender.py::test_dataset_summary_shape PASSED<br/><br/>"
    "============================== 9 passed in 1.20s "
    "===============================</font>", styles["Body"]))
story.append(Paragraph(
    "Run with: <font face='Courier'>python -m pytest tests/ -v</font>", styles["Body"]))

# ---------------- 11. CHALLENGES FACED ----------------
story.append(Paragraph("11. Challenges Faced", styles["H1"]))
challenges = [
    "Balancing how much weight to give genre tags versus free-text overviews in "
    "the TF-IDF input; giving them equal weight produced recommendations that "
    "sometimes matched only on incidental overview wording rather than genre, so "
    "genre text was deliberately repeated to increase its influence.",
    "Handling user typos gracefully without silently guessing wrong -- resolved by "
    "using difflib's fuzzy string matching with a similarity cutoff, combined with "
    "a clear error message (including example titles) when no reasonable match "
    "exists.",
    "Keeping the ML core (recommender.py) unit-testable independently of the "
    "terminal -- resolved by strictly separating I/O (cli.py) from computation "
    "(recommender.py, analytics.py), so tests can call the ML logic directly "
    "without simulating keyboard input.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in challenges],
    bulletType="bullet"))

# ---------------- 12. LEARNINGS & KEY TAKEAWAYS ----------------
story.append(Paragraph("12. Learnings &amp; Key Takeaways", styles["H1"]))
story.append(Paragraph(
    "Building CineMatch reinforced that a correct, well-scoped classical ML "
    "technique (TF-IDF + cosine similarity) can produce genuinely useful results "
    "without needing large datasets, GPUs, or external APIs. It also reinforced "
    "the value of separating concerns early: because ingestion, feature "
    "engineering, the ML core, and presentation were split into distinct modules "
    "from the start, each could be tested and debugged independently, which made "
    "the fuzzy-matching and error-handling additions straightforward to bolt on "
    "later without touching the ML logic itself.", styles["Body"]))

# ---------------- 13. FUTURE ENHANCEMENTS ----------------
story.append(Paragraph("13. Future Enhancements", styles["H1"]))
future = [
    "Incorporate collaborative filtering once real user-rating data is available, "
    "and blend it with the existing content-based scores (a hybrid recommender).",
    "Replace TF-IDF with sentence embeddings (e.g. from a small transformer model) "
    "for deeper semantic matching beyond exact word overlap.",
    "Wrap the existing recommendation engine in a lightweight web UI while "
    "reusing src/recommender.py and src/analytics.py unchanged.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in future],
    bulletType="bullet"))

# ---------------- 14. REFERENCES ----------------
story.append(Paragraph("14. References", styles["H1"]))
refs = [
    "Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. "
    "Journal of Machine Learning Research, 12, 2825-2830.",
    "scikit-learn documentation -- TfidfVectorizer and cosine_similarity "
    "(scikit-learn.org).",
    "pandas documentation (pandas.pydata.org).",
    "Python difflib documentation -- SequenceMatcher-based fuzzy string matching "
    "(docs.python.org).",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["Body"])) for t in refs],
    bulletType="bullet"))

doc = SimpleDocTemplate("CineMatch_Project_Report.pdf", pagesize=A4,
                         topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                         leftMargin=1.8 * cm, rightMargin=1.8 * cm)
doc.build(story)
print("Report built: CineMatch_Project_Report.pdf")
