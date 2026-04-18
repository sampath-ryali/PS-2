"""
Dataset generation for nutrition label OCR.

Generates synthetic or processes real nutrition label images
for training and validation purposes.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatasetGenerator:
    """Generates nutrition label datasets."""

    def __init__(self, output_dir: str = "dataset"):
        """
        Initialize dataset generator.

        Args:
            output_dir: Output directory for dataset
        """
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.metadata: List[Dict[str, Any]] = []

    def add_image_metadata(
        self,
        image_id: str,
        filename: str,
        labels: Dict[str, Any],
        split: str = "train",
    ) -> None:
        """
        Add image metadata to dataset.

        Args:
            image_id: Unique identifier for the image
            filename: Image filename
            labels: Dictionary of extracted nutrition labels
            split: Dataset split (train/val/test)
        """
        metadata_entry = {
            "id": image_id,
            "filename": filename,
            "labels": labels,
            "split": split,
        }
        self.metadata.append(metadata_entry)
        logger.info(f"Added metadata for image: {image_id}")

    def save_metadata(self) -> None:
        """Save metadata to JSON file."""
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_path}")


def main():
    """Main entry point for dataset generation."""
    generator = DatasetGenerator()

    # Example: Add sample metadata
    sample_labels = {
        "product_name": "Sample Nutrition Label",
        "serving_size": "1 cup",
        "calories": 150,
        "fat": 5,
        "protein": 10,
        "carbohydrates": 20,
    }

    generator.add_image_metadata(
        image_id="sample_001",
        filename="nutrition_label_001.jpg",
        labels=sample_labels,
        split="train",
    )

    generator.save_metadata()
    logger.info("Dataset generation complete")


if __name__ == "__main__":
    main()
