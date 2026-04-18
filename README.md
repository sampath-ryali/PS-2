# Food VLM Project - Nutrition Label Analysis System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A production-ready AI-powered system for extracting structured nutrition information from food labels using **PaddleOCR** and **Phi-3 Mini LLM**.

## 🎯 Key Features

✅ **PaddleOCR Integration** - Fast, accurate text detection from nutrition labels  
✅ **Phi-3 Mini LLM** - Local inference, no API keys (3.8B parameters, MIT licensed)  
✅ **Intelligent Routing** - Simple questions use rules, complex ones use AI  
✅ **Confidence Scoring** - Reliability metrics for every extraction  
✅ **Health Analysis** - Score nutrition profiles (1-10) with recommendations  
✅ **OCR Caching** - 50-1500x speedup on repeated images  
✅ **Fully Offline** - No external API calls required  
✅ **GPU/CPU Auto-Detection** - Works with or without GPU  
✅ **Minimal Dependencies** - Only essential packages included  

## 📁 Project Structure

```
food_vlm_project/
├── backend/              # Core inference engine
│   ├── core/
│   │   ├── inference.py       # OCR + extraction pipeline
│   │   └── requirements.txt   # Backend dependencies
│   ├── api/               # REST API (coming soon)
│   └── README.md
├── frontend/              # Streamlit web application
│   ├── streamlit_app.py       # Main UI
│   └── README.md
├── data/                  # Datasets and generation
│   ├── dataset/           # Nutrition label images
│   ├── generation/        # Dataset creation tools
│   └── README.md
├── tests/                 # Unit and integration tests
│   └── test.py
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System design
│   ├── SETUP.md          # Installation guide
│   └── ...
├── requirements.txt       # Root dependencies
├── .gitignore
└── README.md (this file)
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/sampath-ryali/food_vlm_project.git
cd food_vlm_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run frontend/streamlit_app.py
```

The app opens at `http://localhost:8501`

## 📋 What It Does

1. **Upload** a nutrition label image
2. **OCR Processing** - PaddleOCR extracts all visible text
3. **Intelligent Extraction** - Identifies and structures nutrition data
4. **Confidence Scoring** - Rates extraction reliability (high/medium/low)
5. **Health Analysis** - Generates health score (1-10) with personalized recommendations
6. **Display Results** - Shows extracted nutrition, health score, and diet suitability

## 🔧 System Requirements

- Python 3.8+
- 2GB+ RAM (4GB+ recommended)
- GPU optional (auto-detects CPU fallback)

### GPU Setup (Optional)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📚 Documentation

- [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) - System design and component overview
- [**SETUP.md**](docs/SETUP.md) - Detailed installation and troubleshooting
- [**PRODUCTION_README.md**](PRODUCTION_README.md) - Production deployment guide
- [**TECHNICAL_REFERENCE.md**](TECHNICAL_REFERENCE.md) - API and technical details
- [**CPU_ONLY_REFACTORING.md**](CPU_ONLY_REFACTORING.md) - Memory optimization

## 💡 Core Components

### Backend (`backend/core/inference.py`)
- **NutritionExtractor** - Regex-based extraction with 30+ patterns
- **PHI3Extractor** - LLM-based intelligent extraction
- **HealthAnalyzer** - Health scoring and recommendations
- **OCRCaching** - Caching layer for performance

### Frontend (`frontend/streamlit_app.py`)
- Intuitive image upload interface
- Real-time processing display
- Nutrition data visualization
- Health analysis and recommendations

## 🤖 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Text Detection** | PaddleOCR |
| **Language Model** | Phi-3 Mini (3.8B params) |
| **Frontend** | Streamlit |
| **Backend** | Python 3.8+ |
| **ML Framework** | PyTorch |
| **Model Hub** | Hugging Face Transformers |

## 📊 Performance

- **OCR Processing**: ~1-3 seconds per image
- **Extraction**: ~0.5-1 second
- **Health Analysis**: <100ms
- **Cache Hit**: <10ms

## ✨ Extraction Capabilities

**Automatically extracts:**
- Calories/Energy
- Protein
- Carbohydrates
- Fat
- Fiber
- Sugar
- Sodium
- And 20+ additional nutrients

## 🔐 Security & Privacy

- ✅ 100% offline processing
- ✅ No data sent to external services
- ✅ No API keys required
- ✅ All processing on local machine

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions:
1. Check [troubleshooting guide](docs/SETUP.md#troubleshooting)
2. Review [technical reference](TECHNICAL_REFERENCE.md)
3. Open an issue on GitHub

## 🎓 Citation

If you use this project in research, please cite:
```bibtex
@software{food_vlm_2024,
  title={Food VLM Project: Nutrition Label Analysis System},
  author={Ryali, Sampath},
  year={2024},
  url={https://github.com/sampath-ryali/food_vlm_project}
}
```

---

**Status**: ✅ Production Ready | **Version**: 2.0 | **Last Updated**: April 2024
