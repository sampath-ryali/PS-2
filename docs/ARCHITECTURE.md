# System Architecture

## Overview

The Food VLM Project is a production-ready nutrition label analysis system that combines:
- **PaddleOCR**: Fast and accurate text detection
- **Phi-3 Mini LLM**: Intelligent field extraction (3.8B parameters, MIT licensed)
- **Streamlit Frontend**: User-friendly web interface

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                      │
│  - Image Upload Interface                                    │
│  - Results Visualization                                     │
│  - Health Analysis Display                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND - OCR Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│  1. Image Input                                              │
│     └─ Preprocessing & normalization                         │
│  2. PaddleOCR Text Detection                                │
│     └─ Extract all text from image                          │
│  3. Intelligent Routing                                      │
│     ├─ Simple questions → Rule-based extraction             │
│     └─ Complex questions → Phi-3 Mini LLM                   │
│  4. Extraction & Confidence Scoring                         │
│  5. Health Analysis Module                                  │
│     └─ Health scores + recommendations                      │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  - Dataset Storage                                           │
│  - Metadata Management                                       │
│  - Data Generation Tools                                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Backend/Core (inference.py)
- **NutritionExtractor**: Regex-based field extraction
- **PHI3Extractor**: LLM-based intelligent extraction
- **HealthAnalyzer**: Health scoring and recommendations
- **OCRCaching**: Optimization layer for repeated images

### Frontend (streamlit_app.py)
- Image upload and processing
- Real-time result display
- Health analysis visualization

## Processing Flow

1. User uploads nutrition label image
2. System preprocesses the image
3. PaddleOCR extracts all visible text
4. System routes to appropriate extraction method:
   - Rule-based for common fields
   - Phi-3 Mini for complex extraction
5. Results scored for confidence
6. Health analysis applied
7. UI displays formatted results

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Text Detection | PaddleOCR |
| LLM | Phi-3 Mini (3.8B params) |
| Frontend | Streamlit |
| Backend | Python 3.8+ |
| Dependencies | PyTorch, transformers |

## Deployment Considerations

- Fully offline - no API calls required
- GPU optional (CPU fallback available)
- Low memory footprint (ideal for edge deployment)
- Docker-ready for containerization
