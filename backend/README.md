# Backend - Nutrition OCR Engine

This directory contains the core inference pipeline for nutrition label OCR processing.

## Structure

### `/core`
Core OCR and extraction pipeline:
- **inference.py**: Main inference engine combining PaddleOCR and Phi-3 Mini LLM
- **requirements.txt**: Backend dependencies

### `/api` (Coming Soon)
REST API endpoints for the OCR service:
- FastAPI or Flask application
- Endpoints for image upload and processing
- Result serving

## Usage

### Setup
```bash
cd backend/core
pip install -r requirements.txt
```

### Run Inference
```python
from inference import OCRPipeline

pipeline = OCRPipeline()
result = pipeline.process_image("path/to/nutrition_label.jpg")
print(result)
```

## Features
- ✅ PaddleOCR text detection
- ✅ Phi-3 Mini LLM for intelligent extraction
- ✅ Confidence scoring
- ✅ Health analysis module
- ✅ Offline processing (no API calls)
- ✅ GPU/CPU auto-detection
