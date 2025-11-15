# src/data_loader.py
import pandas as pd
import os
from pathlib import Path
from config.paths import config
from config.constants import MISSING_VALUES, TARGET_COLUMN, NON_MEDICAL_FEATURES


class DataLoader:
    """Class to handle data loading with flexible path resolution"""

    def __init__(self):
        self.config = config
        self.missing_values = MISSING_VALUES
        self.target_column = TARGET_COLUMN
        self.non_medical_features = NON_MEDICAL_FEATURES

    def find_data_file(self):
        """Find the data file in various possible locations"""
        possible_locations = [
            self.config.raw_data_file,
            self.config.data_dir / "Dementia Prediction Dataset.csv",
            self.config.root_dir / "Dementia Prediction Dataset.csv",
            Path("Dementia Prediction Dataset.csv"),
            Path("../Dementia Prediction Dataset.csv"),
        ]

        for location in possible_locations:
            if location.exists():
                print(f" Found data file at: {location}")
                return location

        # If not found, show available files
        print(" Data file not found in expected locations.")
        self._show_available_files()
        return None

    def _show_available_files(self):
        """Show available CSV files to help user identify the correct file"""
        print("\n Searching for CSV files in project directory...")
        csv_files = []

        # Search in common directories
        search_dirs = [
            self.config.root_dir,
            self.config.data_dir,
            self.config.raw_data_dir,
            Path("."),  # Current directory
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                for file_path in search_dir.rglob("*.csv"):
                    csv_files.append(file_path)

        if csv_files:
            print(" Found these CSV files:")
            for csv_file in csv_files:
                print(f"   - {csv_file}")
        else:
            print("   No CSV files found!")

        print(f"\n Please ensure your data file is in one of these locations:")
        print(f"   - {self.config.raw_data_dir}/")
        print(f"   - {self.config.data_dir}/")
        print(f"   - Project root directory")

    def load_data(self, usecols=None, nrows=None):
        """Load the main dataset with error handling"""

        data_file = self.find_data_file()
        if data_file is None:
            raise FileNotFoundError(
                "Data file not found. Please ensure 'Dementia Prediction Dataset.csv' "
                "is in the data/raw/ directory or project root."
            )

        try:
            # First, check what columns are available
            available_cols = pd.read_csv(data_file, nrows=0).columns.tolist()
            print(f" File has {len(available_cols)} total columns")

            # If usecols specified, filter to available ones
            if usecols:
                cols_to_load = [col for col in usecols if col in available_cols]
                print(f" Loading {len(cols_to_load)} specified columns")
            else:
                cols_to_load = None

            # Load the data
            df = pd.read_csv(
                data_file,
                usecols=cols_to_load,
                na_values=self.missing_values,
                nrows=nrows  # Useful for testing with subset
            )

            print(f" Successfully loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
            return df

        except Exception as e:
            print(f" Error loading data: {e}")
            raise

    def load_non_medical_data(self, nrows=None):
        """Load only non-medical features and target"""
        cols_to_load = [self.target_column] + [
            col for col in self.non_medical_features
            if col != self.target_column
        ]

        return self.load_data(usecols=cols_to_load, nrows=nrows)


# Create a default instance
data_loader = DataLoader()