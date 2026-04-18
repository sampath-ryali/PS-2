import re
import matplotlib.pyplot as plt

# =========================
# HELPERS
# =========================
def extract_number(value):
    return float(re.search(r"\d+", value).group()) if value != "Not found" else 0


# =========================
# HEALTH ANALYSIS
# =========================
def analyze_health(data):
    protein = extract_number(data["protein"])
    carbs = extract_number(data["carbs"])
    fat = extract_number(data["fat"])
    sodium = extract_number(data["sodium"])

    score = 5
    insights = []

    if protein > 15:
        score += 2
        insights.append("High protein")

    if carbs > 40:
        score -= 2
        insights.append("High carbs")

    if sodium > 500:
        score -= 2
        insights.append("High sodium")

    if fat > 20:
        score -= 1
        insights.append("High fat")

    score = max(1, min(10, score))

    return {
        "score": score,
        "insights": insights
    }


# =========================
# QUESTION ANSWERING (SMART)
# =========================
def answer_questions(data, questions):
    answers = {}

    for q in questions:
        ql = q.lower()

        calories = extract_number(data["calories"])
        protein = extract_number(data["protein"])
        fat = extract_number(data["fat"])
        carbs = extract_number(data["carbs"])
        sodium = extract_number(data["sodium"])

        # CALORIES
        if "calorie" in ql:
            answers[q] = {
                "answer": f"{calories} kcal",
                "reason": "Direct value from nutrition label"
            }

        # FAT
        elif "fat" in ql:
            if fat < 5:
                level = "Low"
            elif fat < 15:
                level = "Moderate"
            else:
                level = "High"

            answers[q] = {
                "answer": level,
                "reason": f"Fat is {fat}g"
            }

        # PROTEIN
        elif "protein" in ql:
            answers[q] = {
                "answer": f"{protein} g",
                "reason": "Taken from label"
            }

        # CARBS
        elif "carb" in ql:
            answers[q] = {
                "answer": f"{carbs} g",
                "reason": "Taken from label"
            }

        # HEALTH
        elif "healthy" in ql:
            analysis = analyze_health(data)
            score = analysis["score"]

            reasons = []

            if protein < 5:
                reasons.append("low protein")
            elif protein > 15:
                reasons.append("high protein")

            if carbs > 40:
                reasons.append("high carbs")

            if fat > 20:
                reasons.append("high fat")

            if sodium > 500:
                reasons.append("high sodium")

            if score >= 7:
                label = "Healthy"
            elif score >= 4:
                label = "Moderate"
            else:
                label = "Unhealthy"

            answers[q] = {
                "answer": label,
                "reason": ", ".join(reasons) if reasons else "balanced nutrition"
            }

        else:
            answers[q] = {
                "answer": "Unknown",
                "reason": "Unsupported question"
            }

    return answers


# =========================
# DIET RECOMMENDATION
# =========================
def recommend_diet(data):
    protein = extract_number(data["protein"])
    carbs = extract_number(data["carbs"])
    fat = extract_number(data["fat"])

    rec = []

    if protein > 15:
        rec.append("Good for muscle gain")

    if carbs < 20:
        rec.append("Low carb friendly")

    if fat > 20:
        rec.append("Avoid for weight loss")

    if not rec:
        rec.append("Balanced diet")

    return rec


# =========================
# RANK PRODUCTS
# =========================
def rank_products(results):
    ranked = []

    for i, r in enumerate(results):
        analysis = analyze_health(r["data"])

        ranked.append({
            "product": f"Product {i+1}",
            "score": analysis["score"],
            "insights": analysis["insights"],
            "data": r["data"]
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


# =========================
# EXPLAIN WINNER (SMART)
# =========================
def explain_winner(ranking):
    best = ranking[0]
    data = best["data"]

    protein = extract_number(data["protein"])
    carbs = extract_number(data["carbs"])
    fat = extract_number(data["fat"])
    sodium = extract_number(data["sodium"])

    reasons = []

    if protein > 10:
        reasons.append("higher protein")

    if carbs < 30:
        reasons.append("lower carbs")

    if sodium < 300:
        reasons.append("lower sodium")

    if fat < 15:
        reasons.append("moderate fat")

    if not reasons:
        reasons.append("balanced nutrition")

    return {
        "winner": best["product"],
        "reason": f"{best['product']} is better due to " + ", ".join(reasons)
    }


# =========================
# VISUALIZATION
# =========================
def plot_comparison(processed_data):

    products = []
    calories = []
    protein = []
    fat = []
    carbs = []

    for i, d in enumerate(processed_data):
        products.append(f"P{i+1}")

        calories.append(extract_number(d["calories"]))
        protein.append(extract_number(d["protein"]))
        fat.append(extract_number(d["fat"]))
        carbs.append(extract_number(d["carbs"]))

    x = range(len(products))

    plt.figure()
    plt.bar(x, calories)
    plt.xticks(x, products)
    plt.title("Calories Comparison")
    plt.show()

    plt.figure()
    plt.bar(x, protein)
    plt.xticks(x, products)
    plt.title("Protein Comparison")
    plt.show()

    plt.figure()
    plt.bar(x, fat)
    plt.xticks(x, products)
    plt.title("Fat Comparison")
    plt.show()

    plt.figure()
    plt.bar(x, carbs)
    plt.xticks(x, products)
    plt.title("Carbs Comparison")
    plt.show()