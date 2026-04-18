# Ollama Setup for Nutrition OCR

This project now uses **Ollama + Phi-3 Mini** for lightweight reasoning without PyTorch issues.

## Installation & Setup (5 minutes)

### Step 1: Install Ollama
- Download from [ollama.ai](https://ollama.ai)
- Install the Windows version
- Accept all prompts during installation

### Step 2: Pull the Phi-3 Model
Open PowerShell or Command Prompt and run:
```powershell
ollama pull phi
```

This downloads the Phi-3 Mini model (~2.3GB). First time takes a few minutes.

### Step 3: Start Ollama Server
```powershell
ollama serve
```

Keep this terminal open. Ollama runs on `http://localhost:11434`

### Step 4: Test Your Questions
In another terminal, run:
```powershell
python test/test.py
```

## How It Works

- **Rule-based questions** (calories, protein, fat) → Direct extraction, instant ✅
- **Reasoning questions** (is it healthy, gluten-free, etc.) → Ollama API call, 2-5 seconds ✅
- **No PyTorch crashes** → Ollama runs separately, zero dependency issues ✅

## Example Output

```
[4] Questions answered (rule-based + reasoning):
    Q: How many calories?
    A: 112 kcal
    Q: How much protein?
    A: 12 g
    Q: What's the fat content?
    A: 12.8 g
    Q: Is this product healthy?
    A: {
        "answer": "Moderately healthy - good protein, moderate calories, reasonable fat",
        "reasoning": "Product has 112 kcal, decent protein content..."
    }
```

## Troubleshooting

**"Ollama server not running"**
- Run `ollama serve` in a separate terminal
- Make sure it stays open

**"Model not found: phi"**
- Run `ollama pull phi` first

**Slow responses (5+ seconds)**
- First inference is slower (model initialization)
- Subsequent calls are faster
- Normal for CPU inference

## Alternative Models

You can use other models instead of `phi`:
```powershell
ollama pull mistral      # Larger, better reasoning
ollama pull neural-chat  # Fast, good quality
ollama pull orca-mini    # Lightweight, good for nutrition
```

Change the MODEL_NAME in `inference.py` if you switch models.

## API Details

The code calls Ollama's REST API:
```
POST http://localhost:11434/api/generate
{
    "model": "phi",
    "prompt": "...",
    "stream": false,
    "temperature": 0.7
}
```

No authentication needed when running locally.
