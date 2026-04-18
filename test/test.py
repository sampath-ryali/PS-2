import sys
import os
import json

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference.inference import (
    analyze_health,
    recommend_diet,
    answer_questions,
    rank_products,
    explain_winner,
    plot_comparison
)

# =========================
# LOAD DATA
# =========================
metadata_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dataset", "metadata.json")
)

with open(metadata_path, 'r') as f:
    metadata = json.load(f)

# Use valid indices
indices = [0, 1, 2]

questions = [
    "How many calories?",
    "Is fat high?",
    "How much protein?",
    "Is this healthy?"
]

processed_data = []

# =========================
# PRINT HEADER
# =========================
print("=" * 60)
print("🧠 SMART NUTRITION SYSTEM REPORT")
print("=" * 60)

# =========================
# PROCESS PRODUCTS
# =========================
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
    print("-" * 60)

    # DATA
    print("📊 Data:")
    for k, v in data.items():
        print(f"   {k.capitalize():<10}: {v}")

    # HEALTH
    health = analyze_health(data)
    print(f"\n❤️ Health Score: {health['score']} / 10")

    print("⚠️ Insights:")
    if health["insights"]:
        for ins in health["insights"]:
            print(f"   - {ins}")
    else:
        print("   - None")

    # DIET
    print("\n🥗 Diet Recommendation:")
    for d in recommend_diet(data):
        print(f"   - {d}")

    # Q&A
    print("\n💬 Q&A:")
    answers = answer_questions(data, questions)

    for q, a in answers.items():
        print(f"\n   ➤ {q}")

        if isinstance(a, dict):
            print(f"     → {a.get('answer')}")
            print(f"     Reason: {a.get('reason')}")
        else:
            print(f"     → {a}")

# =========================
# RANKING
# =========================
print("\n" + "=" * 60)
print("🏆 FINAL RANKING")
print("=" * 60)

results = [{"data": d} for d in processed_data]
ranking = rank_products(results)

medals = ["🥇", "🥈", "🥉"]

for i, r in enumerate(ranking):
    medal = medals[i] if i < len(medals) else "🔹"
    print(f"{medal} {r['product']} → Score: {r['score']}")

# =========================
# WINNER
# =========================
winner = explain_winner(ranking)

print("\n🎯 WINNER:", winner["winner"])
print("Reason:")
print(winner["reason"])

# =========================
# VISUALS
# =========================
plot_comparison(processed_data)

print("\n" + "=" * 60)
print("✅ SYSTEM RUN COMPLETE")
print("=" * 60)