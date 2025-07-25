# utils/feedback.py

import os
import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "data/feedback.csv"

def save_feedback(feature_request: str):
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[timestamp, feature_request]], columns=["Timestamp", "Feedback"])

    if os.path.exists(FEEDBACK_FILE):
        existing = pd.read_csv(FEEDBACK_FILE)
        combined = pd.concat([existing, new_entry], ignore_index=True)
    else:
        combined = new_entry

    combined.to_csv(FEEDBACK_FILE, index=False)
