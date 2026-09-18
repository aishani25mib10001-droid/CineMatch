"""
make_diagrams.py
-----------------
One-off script that generates the design diagrams (architecture,
workflow, class relationships, use-case) as PNG files using
matplotlib shapes only (no external diagram service needed, keeping
the whole project self-contained and offline-runnable).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT_DIR = "."


def box(ax, x, y, w, h, text, color="#4C72B0", fontsize=10, textcolor="white"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=1.4, edgecolor="#2c3e50", facecolor=color)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=textcolor, weight="bold", wrap=True)
    return (x, y, w, h)


def arrow(ax, start, end, label=None, color="#2c3e50"):
    a = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                         linewidth=1.6, color=color)
    ax.add_patch(a)
    if label:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + 0.1, label, ha="center", fontsize=8, color=color, style="italic")


# ---------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("CineMatch — System Architecture", fontsize=14, weight="bold")

box(ax, 0.5, 5.3, 2.2, 1.0, "movies.csv\n(Dataset)", color="#8c8c8c")
box(ax, 3.3, 5.3, 2.6, 1.0, "data_loader.py\n(Ingestion)", color="#4C72B0")
box(ax, 6.4, 5.3, 3.0, 1.0, "preprocessor.py\n(TF-IDF Vectorization)", color="#4C72B0")

box(ax, 6.4, 3.4, 3.0, 1.0, "recommender.py\n(Cosine Similarity ML Core)", color="#DD8452")

box(ax, 3.3, 1.5, 2.6, 1.0, "cli.py\n(User Interaction)", color="#55A868")
box(ax, 6.4, 1.5, 3.0, 1.0, "analytics.py\n(Reporting)", color="#55A868")
box(ax, 0.5, 1.5, 2.2, 1.0, "main.py\n(Entry Point)", color="#C44E52")
box(ax, 0.5, 3.4, 2.2, 1.0, "logger_config.py\n/ config.py", color="#8172B2")

arrow(ax, (2.7, 5.8), (3.3, 5.8))              # dataset -> loader
arrow(ax, (5.9, 5.8), (6.4, 5.8))              # loader -> preprocessor
arrow(ax, (7.9, 5.3), (7.9, 4.4))              # preprocessor -> ML core
arrow(ax, (6.4, 3.7), (5.9, 2.3), label="ranked scores")   # ML core -> cli
arrow(ax, (1.6, 2.2), (3.3, 2.2), label="user query")       # main -> cli
arrow(ax, (5.9, 1.8), (6.4, 1.8))              # cli -> analytics
arrow(ax, (3.3, 1.7), (1.6, 1.7), color="#7f8c8d")          # cli -> main (printed output)

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/architecture_diagram.png", dpi=150)
plt.close()


# ---------------------------------------------------------------
# 2. PROCESS FLOW / WORKFLOW DIAGRAM
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 9))
ax.set_xlim(-0.9, 5.4)
ax.set_ylim(0, 13)
ax.axis("off")
ax.set_title("CineMatch — Workflow", fontsize=13, weight="bold")

steps = [
    "Start CLI\n(main.py)",
    "Load movies.csv\n(data_loader)",
    "Valid dataset?",
    "Build content soup\n+ TF-IDF vectorize\n(preprocessor)",
    "Compute cosine\nsimilarity matrix\n(recommender)",
    "Show prompt,\nwait for user input",
    "Command type?",
    "Print similarity-\nranked recommendations",
    "Print catalogue /\nanalytics report",
    "Exit",
]
ys = [12, 10.6, 9.2, 7.8, 6.4, 5.0, 3.6, 2.2, 2.2, 0.4]
xs = [1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 0.3, 3.4, 1.9]

colors = ["#4C72B0", "#4C72B0", "#DD8452", "#4C72B0", "#DD8452",
          "#55A868", "#DD8452", "#55A868", "#55A868", "#C44E52"]

boxes = []
for i, (s, y, x, c) in enumerate(zip(steps, ys, xs, colors)):
    w = 2.6 if i not in (7, 8) else 2.0
    b = box(ax, x, y, w, 1.1, s, color=c, fontsize=8.5)
    boxes.append((x + w / 2, y))

for i in range(len(boxes) - 3):
    arrow(ax, (boxes[i][0], boxes[i][1]), (boxes[i + 1][0], boxes[i + 1][1] + 1.1))

arrow(ax, (1.9 + 1.0, ys[6] + 0.2), (1.3, ys[7] + 1.1), label="title")
arrow(ax, (1.9 + 1.6, ys[6] + 0.2), (4.4, ys[8] + 1.1), label="stats/list")
arrow(ax, (1.3, ys[7]), (3.0, ys[9] + 1.1))
arrow(ax, (4.4, ys[8]), (3.0, ys[9] + 1.1))
# loop back: after printing results, CLI returns to the prompt (repeats until quit)
loop = FancyArrowPatch((0.3, ys[7] + 0.55), (0.05, ys[5] + 0.55),
                        connectionstyle="arc3,rad=0.6", arrowstyle="-|>",
                        mutation_scale=14, linewidth=1.4, color="#7f8c8d", linestyle="--")
ax.add_patch(loop)
ax.text(-0.35, (ys[7] + ys[5]) / 2 + 1.2, "loop\nuntil\nquit", fontsize=7, color="#7f8c8d", ha="center")

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/workflow_diagram.png", dpi=150)
plt.close()


# ---------------------------------------------------------------
# 3. CLASS / COMPONENT DIAGRAM (simplified UML)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("CineMatch — Class / Component Diagram (simplified UML)", fontsize=13, weight="bold")


def uml_class(ax, x, y, w, h, name, attrs, methods):
    b = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.02",
                        linewidth=1.4, edgecolor="#2c3e50", facecolor="#f7f7f7")
    ax.add_patch(b)
    ax.plot([x, x + w], [y + h - 0.5, y + h - 0.5], color="#2c3e50", linewidth=1)
    split_y = y + h - 0.5 - 0.35 * len(attrs) - 0.15
    ax.plot([x, x + w], [split_y, split_y], color="#2c3e50", linewidth=1)
    ax.text(x + w / 2, y + h - 0.28, name, ha="center", fontsize=9.5, weight="bold")
    for i, a in enumerate(attrs):
        ax.text(x + 0.15, y + h - 0.75 - 0.32 * i, a, fontsize=7.8, family="monospace")
    for i, m in enumerate(methods):
        ax.text(x + 0.15, split_y - 0.3 - 0.32 * i, m, fontsize=7.8, family="monospace")


uml_class(ax, 0.3, 3.6, 2.7, 2.1, "RecommendationEngine",
          ["- df", "- similarity_matrix", "- titles"],
          ["+ recommend(title, n)", "- _resolve_title(query)"])

uml_class(ax, 3.5, 3.6, 2.7, 1.7, "DataLoader",
          ["+ REQUIRED_COLUMNS"],
          ["+ load_movies(path)"])

uml_class(ax, 6.7, 3.6, 2.9, 1.9, "Preprocessor",
          [],
          ["+ build_content_soup(df)", "+ vectorize(df)"])

uml_class(ax, 3.5, 0.6, 2.7, 1.8, "AnalyticsReporter",
          [],
          ["+ genre_distribution(df)", "+ dataset_summary(df)",
           "+ format_summary_report(df)"])

uml_class(ax, 6.7, 0.6, 2.9, 1.8, "CLI",
          ["- engine: RecommendationEngine"],
          ["+ run()"])

arrow(ax, (4.9, 3.6), (4.9, 2.4))          # DataLoader -> AnalyticsReporter (feeds df)
arrow(ax, (8.15, 2.4), (8.15, 3.6))        # CLI -> Preprocessor (calls vectorize)
arrow(ax, (6.7, 1.5), (6.2, 1.5))          # CLI -> AnalyticsReporter (calls format_summary_report)
arrow(ax, (6.7, 4.6), (6.2, 4.6))          # Preprocessor -> DataLoader (consumes df)
arrow(ax, (1.65, 4.3), (3.5, 3.9))         # DataLoader -> RecommendationEngine (feeds df)


plt.tight_layout()
plt.savefig(f"{OUT_DIR}/class_diagram.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 4. USE CASE DIAGRAM
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 8)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("CineMatch — Use Case Diagram", fontsize=13, weight="bold")

# Actor (simple stick figure)
def actor(ax, x, y, label):
    ax.plot(x, y + 1.1, 'o', markersize=14, markerfacecolor="#f4d35e",
            markeredgecolor="#2c3e50", markeredgewidth=1.5)
    ax.plot([x, x], [y + 0.15, y + 0.85], color="#2c3e50", linewidth=2)
    ax.plot([x - 0.35, x + 0.35], [y + 0.65, y + 0.65], color="#2c3e50", linewidth=2)
    ax.plot([x, x - 0.3], [y + 0.15, y - 0.25], color="#2c3e50", linewidth=2)
    ax.plot([x, x + 0.3], [y + 0.15, y - 0.25], color="#2c3e50", linewidth=2)
    ax.text(x, y - 0.55, label, ha="center", fontsize=9, weight="bold")


def oval(ax, x, y, w, h, text):
    e = mpatches.Ellipse((x, y), w, h, edgecolor="#2c3e50",
                          facecolor="#EBF3FB", linewidth=1.4)
    ax.add_patch(e)
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5)


actor(ax, 0.9, 3.6, "Student\n(User)")

use_cases = [
    (4.0, 6.5, 2.6, 1.0, "Get movie\nrecommendations"),
    (4.0, 5.0, 2.6, 1.0, "View full\ncatalogue"),
    (4.0, 3.5, 2.6, 1.0, "View dataset\nanalytics"),
    (4.0, 2.0, 2.6, 1.0, "Exit\napplication"),
]
for (x, y, w, h, t) in use_cases:
    oval(ax, x, y, w, h, t)
    arrow(ax, (1.3, 4.15), (x - w / 2, y))

# system boundary box
boundary = FancyBboxPatch((2.4, 1.2), 4.0, 6.0, boxstyle="square,pad=0.02",
                           linewidth=1.2, edgecolor="#888888", facecolor="none",
                           linestyle="--")
ax.add_patch(boundary)
ax.text(4.4, 7.35, "CineMatch CLI", fontsize=9, color="#666666", weight="bold")

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/use_case_diagram.png", dpi=150)
plt.close()


# ---------------------------------------------------------------
# 5. SEQUENCE DIAGRAM (get recommendations, happy path)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))
ax.set_xlim(0, 9)
ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("CineMatch — Sequence Diagram: 'Get Recommendations'", fontsize=12, weight="bold")

lifelines = [
    (1.0, "User"),
    (3.0, "CLI"),
    (5.2, "RecommendationEngine"),
    (7.6, "AnalyticsReporter\n(not used here)"),
]
for x, name in lifelines:
    ax.text(x, 6.6, name, ha="center", fontsize=8.5, weight="bold")
    ax.plot([x, x], [0.4, 6.3], color="#b0b0b0", linewidth=1.2, linestyle="--")

messages = [
    (1.0, 3.0, 5.8, "types movie title"),
    (3.0, 5.2, 5.2, "recommend(title, top_n=5)"),
    (5.2, 5.2, 4.6, "_resolve_title(query)"),
    (5.2, 3.0, 4.0, "ranked DataFrame (title, genres, similarity)"),
    (3.0, 1.0, 3.2, "prints top 5 recommendations"),
]
for x1, x2, y, label in messages:
    color = "#2c3e50"
    if x1 == x2:  # self-call
        ax.annotate("", xy=(x1 + 0.6, y - 0.15), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
        ax.annotate("", xy=(x1, y - 0.3), xytext=(x1 + 0.6, y - 0.15),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
        ax.text(x1 + 0.7, y - 0.15, label, fontsize=7.5, va="center")
    else:
        style = "-|>" if x2 > x1 or label.startswith("prints") else "-|>"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.3))
        ax.text((x1 + x2) / 2, y + 0.15, label, ha="center", fontsize=7.5)

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/sequence_diagram.png", dpi=150)
plt.close()


print("Diagrams generated: architecture, workflow, class, use_case, sequence")
