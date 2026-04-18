# Setup and Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) GPU with CUDA support for faster inference

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/sampath-ryali/food_vlm_project.git
cd food_vlm_project
```

### 2. Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Or install backend-specific requirements
pip install -r backend/core/requirements.txt
```

### 3. Run the Application

```bash
# Run Streamlit frontend
streamlit run frontend/streamlit_app.py
```

The application will open at `http://localhost:8501`

## GPU Setup (Optional)

For GPU acceleration with CUDA:

```bash
# For NVIDIA GPUs
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## CPU-Only Setup

The system automatically falls back to CPU if GPU is not available.

## Docker Setup (Coming Soon)

```bash
docker build -t nutrition-ocr .
docker run -p 8501:8501 nutrition-ocr
```

## Troubleshooting

### Out of Memory (OOM) Error
See [CPU_ONLY_REFACTORING.md](../CPU_ONLY_REFACTORING.md) for memory optimization tips.

### OLLAMA Setup
For local LLM setup, see [OLLAMA_SETUP.md](../OLLAMA_SETUP.md)

## Next Steps

1. Check [PRODUCTION_README.md](../PRODUCTION_README.md) for production deployment
2. Review [TECHNICAL_REFERENCE.md](../TECHNICAL_REFERENCE.md) for API details
