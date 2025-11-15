# config/paths.py
import os
from pathlib import Path


class PathConfig:
    """Configuration class for managing all project paths"""

    def __init__(self):
        # Root directory (the project folder)
        self.root_dir = Path(__file__).parent.parent

        # Data paths
        self.data_dir = self.root_dir / "data"
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.data_dir / "processed"
        self.external_data_dir = self.data_dir / "external"

        # Results paths
        self.results_dir = self.root_dir / "results"
        self.models_dir = self.results_dir / "models"
        self.visuals_dir = self.results_dir / "visuals"
        self.reports_dir = self.results_dir / "reports"

        # Source code paths
        self.src_dir = self.root_dir / "src"

        # Notebooks path
        self.notebooks_dir = self.root_dir / "notebooks"

        # Expected file names
        self.raw_data_file = self.raw_data_dir / "Dementia Prediction Dataset.csv"
        self.cleaned_data_file = self.processed_data_dir / "cleaned_data.csv"

    def create_directories(self):
        """Create all necessary directories if they don't exist"""
        directories = [
            self.raw_data_dir,
            self.processed_data_dir,
            self.external_data_dir,
            self.models_dir,
            self.visuals_dir / "eda",
            self.visuals_dir / "feature_importance",
            self.visuals_dir / "model_performance",
            self.reports_dir,
            self.src_dir,
            self.notebooks_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f" Created: {directory}")


# Create global config instance
config = PathConfig()