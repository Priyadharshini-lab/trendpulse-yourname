# task2_data_processing.py

import pandas as pd
import os
import json

# Step 1: Load latest JSON file from data folder
def get_latest_json():
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    
    if not files:
        print("No JSON file found!")
        return None
    
    files.sort()
    return os.path.join("data", files[-1])


def main():
    file_path = get_latest_json()
    
    if not file_path:
        return

    # -----------------------------
    # 1. LOAD DATA
    # -----------------------------
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print(f"Loaded {len(df)} stories from {file_path}")

    # -----------------------------
    # 2. CLEAN DATA
    # -----------------------------

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Remove missing important values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Fix data types
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # Remove low quality (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Remove extra whitespace in title
    df["title"] = df["title"].str.strip()

    # -----------------------------
    # 3. SAVE CSV
    # -----------------------------
    output_file = "data/trends_clean.csv"
    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}")

    # -----------------------------
    # SUMMARY
    # -----------------------------
    print("\nStories per category:")
    print(df["category"].value_counts())


# Run script
if __name__ == "__main__":
    main()
