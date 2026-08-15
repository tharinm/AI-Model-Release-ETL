"""
Configuration settings and paths for AI Model Release ETL & Prediction Pipeline.
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Datasets
CSV_DATASET_PATH = PROCESSED_DATA_DIR / "models_dataset.csv"
PARQUET_DATASET_PATH = PROCESSED_DATA_DIR / "models_dataset.parquet"
PREDICTIONS_OUTPUT_PATH = PROCESSED_DATA_DIR / "models_with_predictions.json"
MODEL_SAVE_PATH = PROCESSED_DATA_DIR / "popularity_model.pkl"

# Hugging Face API Settings
HF_MODELS_API_URL = "https://huggingface.co/api/models"
DEFAULT_FETCH_LIMIT = 500

# Required Output Columns
DATASET_COLUMNS = [
    "model_id",
    "author",
    "model_name",
    "model_type",
    "pipeline_tag",
    "downloads",
    "likes",
    "created_at",
    "last_modified",
    "library",
    "license",
    "tags",
    "num_tags",
    "age_days",
    "like_to_download_ratio",
    "popularity_score"
]
