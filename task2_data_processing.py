# task2_data_processing.py

import os
import json
import pandas as pd

# Step 1: Find latest JSON file inside data folder
def get_latest_json_file(folder="data"):
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    if not files:
        print("No JSON files found in data folder!")
        return None
    
    # Sort files by name (latest date last)
    files.sort()
    return os.path.join(folder, files[-1])


def main():
    # Get latest JSON file
    json_file = get_latest_json_file()
    
    if not json_file:
        return
    
    print(f"Loading file: {json_file}")

    # Step 2: Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    print(f"Original records: {len(df)}")

    # -------------------------------
    # Step 3: Data Cleaning
    # -------------------------------

    # Remove duplicates based on post_id
    df = df.drop_duplicates(subset="post_id")

    # Handle missing values
    df["title"] = df["title"].fillna("No Title")
    df["author"] = df["author"].fillna("Unknown")

    # Convert numeric fields safely
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # Convert collected_at to datetime format
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")

    # Remove rows where category is missing (extra safety)
    df = df.dropna(subset=["category"])

    print(f"Cleaned records: {len(df)}")

    # -------------------------------
    # Step 4: Save as CSV
    # -------------------------------

    # Create output file name
    output_file = json_file.replace(".json", ".csv")

    df.to_csv(output_file, index=False)

    print(f"Cleaned data saved to: {output_file}")


# Run script
if __name__ == "__main__":
    main()
