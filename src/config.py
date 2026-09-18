"""
config.py
----------
Central configuration for CineMatch. Keeping paths and tunable
parameters in one place satisfies the Maintainability non-functional
requirement -- nothing below needs to be hunted down inside logic files
if the dataset location or recommendation size changes.
"""

import os

# Base directory of the whole project (one level above src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset location. Swapping this single value lets CineMatch run on a
# larger or different movie catalogue without touching any other module
# -> this is what gives the system its Scalability property.
DATA_PATH = os.path.join(BASE_DIR, "data", "movies.csv")

# Log file location (Logging / Monitoring non-functional requirement)
LOG_PATH = os.path.join(BASE_DIR, "cinematch.log")

# How many recommendations to return by default
DEFAULT_TOP_N = 5

# TF-IDF settings used by the ML core (Recommendation Engine module)
TFIDF_STOP_WORDS = "english"
