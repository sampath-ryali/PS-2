import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference.inference import (
    analyze_health,
    recommend_diet,
    answer_questions,
    rank_products,
    explain_winner,
    plot_comparison
)

# LOAD DATA
metadata_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dataset", "metadata.json")
)

with open(metadata_path, 'r') as f:
    metadata = json.load(f)

indices = [5, 10, 15]

questions = [
    "How many calories?",
    "Is fat high?",
    "How much protein?",
    "Is this healthy?"
]

processed_data = []

print("=" * 60)
print("SMART NUTRITION SYSTEM")
print("=" * 60)

for idx, i in enumerate(indices):
    img = metadata[i]

    data = {
        "calories": img["calories"],
        "fat": img["fat"],
        "protein": img["protein"],
        "carbs": img["carbs"],
        "sodium": img["sodium"]
    }

    processed_data.append(data)

    print(f"\n🔹 PRODUCT {idx+1}")
    print("\n[DATA]", data)

    print("\n[HEALTH]")
    print(analyze_health(data))

    print("\n[DIET]")
    print(recommend_diet(data))

    print("\n[Q&A]")
    print(answer_questions(data, questions))


# RANKING
print("\n" + "=" * 60)
print("🏆 RANKING")
print("=" * 60)

results = [{"data": d} for d in processed_data]
ranking = rank_products(results)

for r in ranking:
    print(f"{r['product']} → Score: {r['score']} | {r['insights']}")

winner = explain_winner(ranking)

print("\n🥇 WINNER")
print(winner)

# VISUALS
plot_comparison(processed_data)

print("\n" + "=" * 60)
print("✅ DONE")
print("=" * 60)