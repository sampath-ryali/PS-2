import re
import matplotlib.pyplot as plt
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# QWEN MODEL MANAGER
# =========================
class QwenModelManager:
    """
    Singleton pattern for Qwen2.5-3B-Instruct model
    - CPU-only mode (no GPU risk)
    - torch.float32 (CPU native)
    - low_cpu_mem_usage=True for memory efficiency
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.model_name = "Qwen/Qwen2.5-3B-Instruct"
        self.device = torch.device("cpu")  # Force CPU
        self.model = None
        self.tokenizer = None
        self._initialized = True
        logger.info(f"QwenModelManager initialized (lazy loading enabled)")
    
    def load_model(self):
        """Lazy load model on first use"""
        if self.model is not None:
            return self.model
        
        logger.info(f"Loading {self.model_name}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map="cpu",
                low_cpu_mem_usage=True
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
        
        return self.model
    
    def answer_question(self, question, nutrition_data):
        """Use Qwen to answer complex nutrition questions"""
        try:
            model = self.load_model()
            
            # Create context from nutrition data
            context = f"""
            Nutrition Information:
            - Calories: {nutrition_data.get('calories', 'Unknown')}
            - Protein: {nutrition_data.get('protein', 'Unknown')}
            - Carbs: {nutrition_data.get('carbs', 'Unknown')}
            - Fat: {nutrition_data.get('fat', 'Unknown')}
            - Sodium: {nutrition_data.get('sodium', 'Unknown')}
            - Fiber: {nutrition_data.get('fiber', 'Unknown')}
            - Sugar: {nutrition_data.get('sugar', 'Unknown')}
            
            Question: {question}
            Answer:
            """
            
            inputs = self.tokenizer(context, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.7,
                    top_p=0.95,
                    do_sample=False
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the answer part
            answer = response.split("Answer:")[-1].strip()
            
            return {
                "answer": answer,
                "source": "Qwen2.5-3B-Instruct",
                "confidence": "medium"
            }
        except Exception as e:
            logger.error(f"Error in Qwen inference: {e}")
            return {
                "answer": "Unable to answer",
                "source": "Qwen2.5-3B-Instruct",
                "confidence": "low",
                "error": str(e)
            }

# Global instance
qwen_manager = QwenModelManager()

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
# QUESTION ANSWERING (SMART ROUTING)
# =========================
def answer_questions(data, questions):
    """
    Smart routing:
    - Simple questions → Rule-based extraction
    - Complex questions → Qwen LLM
    """
    answers = {}
    
    simple_keywords = ["calorie", "fat", "protein", "carb", "sodium", "sugar", "fiber"]
    
    for q in questions:
        ql = q.lower()
        
        # Check if simple question
        is_simple = any(keyword in ql for keyword in simple_keywords)
        
        if is_simple:
            # Rule-based extraction for simple questions
            answers[q] = _answer_simple_question(q, data)
        else:
            # Use Qwen for complex questions
            answers[q] = qwen_manager.answer_question(q, data)
    
    return answers


def _answer_simple_question(q, data):
    """Handle simple nutrition questions with rules"""
    ql = q.lower()
    
    calories = extract_number(data.get("calories", "Not found"))
    protein = extract_number(data.get("protein", "Not found"))
    fat = extract_number(data.get("fat", "Not found"))
    carbs = extract_number(data.get("carbs", "Not found"))
    sodium = extract_number(data.get("sodium", "Not found"))
    
    # CALORIES
    if "calorie" in ql:
        answer = {
            "answer": f"{calories} kcal",
            "reason": "Direct value from nutrition label",
            "source": "Rule-based"
        }

    # FAT
    elif "fat" in ql:
        if fat < 5:
            level = "Low"
        elif fat < 15:
            level = "Moderate"
        else:
            level = "High"

        answer = {
            "answer": level,
            "reason": f"Fat is {fat}g",
            "source": "Rule-based"
        }

    # PROTEIN
    elif "protein" in ql:
        answer = {
            "answer": f"{protein} g",
            "reason": "Taken from label",
            "source": "Rule-based"
        }

    # CARBS
    elif "carb" in ql:
        answer = {
            "answer": f"{carbs} g",
            "reason": "Taken from label",
            "source": "Rule-based"
        }

    # SODIUM
    elif "sodium" in ql:
        answer = {
            "answer": f"{sodium} mg",
            "reason": "Taken from label",
            "source": "Rule-based"
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
        
        answer = {
            "answer": label,
            "reason": ", ".join(reasons) if reasons else "balanced nutrition",
            "source": "Rule-based"
        }
    
    else:
        answer = {
            "answer": "Unknown",
            "reason": "Unsupported question",
            "source": "Rule-based"
        }
    
    return answer



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