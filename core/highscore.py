# core/highscore.py

import json
import os

SCORE_FILE = "highscore.json"

def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    return 0

def save_high_score(score):
    with open(SCORE_FILE, "w") as f:
        json.dump({"high_score": score}, f)
