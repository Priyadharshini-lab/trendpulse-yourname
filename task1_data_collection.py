# task1_data_collection.py

import requests
import json
import time
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (IMPORTANT as per instructions)
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word.lower() in title_lower:
                return category
    return None  # ignore if no category matched


def fetch_top_story_ids(limit=500):
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story_details(story_id):
    """Fetch individual story details"""
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def main():
    story_ids = fetch_top_story_ids()
    collected_stories = []

    # Track count per category
    category_count = {cat: 0 for cat in categories}

    for story_id in story_ids:
        story = fetch_story_details(story_id)

        if not story or "title" not in story:
            continue

        category = get_category(story["title"])

        # Skip if no category match
        if not category:
            continue

        # Limit 25 stories per category
        if category_count[category] >= 25:
            continue

        # Extract required fields
        extracted = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_stories.append(extracted)
        category_count[category] += 1

        # Stop if total reaches 125
        if len(collected_stories) >= 125:
            break

    # Sleep once per category loop (as required)
    for _ in categories:
        time.sleep(2)

    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")


# Run script
if __name__ == "__main__":
    main()
