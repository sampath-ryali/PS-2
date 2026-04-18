# Data - Datasets and Generation

This directory contains nutrition label datasets and data generation utilities.

## Structure

### `/dataset`
Processed nutrition label images and metadata:
- **images/**: Nutrition label photographs
- **metadata.json**: Ground truth labels and annotations

### `/generation`
Data generation and augmentation tools:
- **generate_dataset.py**: Tools for creating synthetic or augmented datasets

## Dataset Format

Images should be nutrition label photographs in common formats (JPG, PNG).

Metadata format (JSON):
```json
{
  "images": [
    {
      "filename": "label_001.jpg",
      "nutrition": {
        "calories": 150,
        "protein": 8,
        "carbs": 20,
        "fat": 5
      }
    }
  ]
}
```
