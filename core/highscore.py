import pickle
import os

SCORE_FILE = "highscore.dat"

def load_high_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "rb") as f:
                data = pickle.load(f)
                return data.get("high_score", 0)
        except Exception:
            return 0  # Corrupted file or wrong format
    return 0

def save_high_score(score):
    with open(SCORE_FILE, "wb") as f:
        pickle.dump({"high_score": score}, f)
