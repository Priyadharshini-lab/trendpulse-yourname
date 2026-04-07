# task3_analysis.py

import pandas as pd
import numpy as np
import os

def main():
    # -----------------------------
    # 1. LOAD DATA
    # -----------------------------
    file_path = "data/trends_clean.csv"

    if not os.path.exists(file_path):
        print("CSV file not found! Run Task 2 first.")
        return

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} rows from {file_path}")

    # -----------------------------
    # 2. NUMPY STATISTICS
    # -----------------------------

    scores = df["score"].values

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)

    print("\nScore Statistics:")
    print(f"Mean: {mean_score:.2f}")
    print(f"Median: {median_score}")
    print(f"Standard Deviation: {std_score:.2f}")

    # -----------------------------
    # 3. ADD NEW COLUMNS
    # -----------------------------

    # Engagement = score + comments
    df["engagement"] = df["score"] + df["num_comments"]

    # Popular if score > mean
    df["is_popular"] = df["score"] > mean_score

    print("\nNew columns added: engagement, is_popular")

    # -----------------------------
    # EXTRA INSIGHTS (good for marks)
    # -----------------------------

    print("\nTop Category:")
    print(df["category"].value_counts().idxmax())

    print("\nTop Author:")
    print(df["author"].value_counts().idxmax())

    # -----------------------------
    # 4. SAVE NEW CSV
    # -----------------------------

    output_file = "data/trends_analysed.csv"
    df.to_csv(output_file, index=False)

    print(f"\nSaved analysed data to {output_file}")


# Run script
if __name__ == "__main__":
    main()
