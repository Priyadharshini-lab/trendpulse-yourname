# task4_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def shorten_title(title, max_length=50):
    """Shorten long titles for better display in charts"""
    return title if len(title) <= max_length else title[:47] + "..."

def main():
    # -----------------------------
    # 1. LOAD DATA + SETUP
    # -----------------------------
    file_path = "data/trends_analysed.csv"

    if not os.path.exists(file_path):
        print("File not found! Run Task 3 first.")
        return

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} rows")

    # Create outputs folder
    os.makedirs("outputs", exist_ok=True)

    # -----------------------------
    # 2. CHART 1 — TOP 10 STORIES
    # -----------------------------
    top10 = df.sort_values(by="score", ascending=False).head(10)

    titles = top10["title"].apply(shorten_title)
    scores = top10["score"]

    plt.figure()
    plt.barh(titles, scores)
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()

    # -----------------------------
    # 3. CHART 2 — STORIES PER CATEGORY
    # -----------------------------
    category_counts = df["category"].value_counts()

    plt.figure()
    category_counts.plot(kind="bar", color=["red", "blue", "green", "orange", "purple"])
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()

    # -----------------------------
    # 4. CHART 3 — SCATTER PLOT
    # -----------------------------
    plt.figure()

    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.scatter(popular["score"], popular["num_comments"], label="Popular", alpha=0.7)
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular", alpha=0.7)

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()

    # -----------------------------
    # BONUS — DASHBOARD
    # -----------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1
    axes[0].barh(titles, scores)
    axes[0].set_title("Top 10 Stories")
    axes[0].invert_yaxis()

    # Chart 2
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular", alpha=0.7)
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular", alpha=0.7)
    axes[2].set_title("Score vs Comments")

    fig.suptitle("TrendPulse Dashboard")

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()

    print("\nAll charts saved in outputs/ folder!")


# Run
if __name__ == "__main__":
    main()
