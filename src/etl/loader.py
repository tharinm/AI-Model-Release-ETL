"""
Loader module for deduplicating model records and storing datasets in CSV & Parquet formats.
"""
import os
import json
import logging
import pandas as pd
from pathlib import Path
from typing import Tuple

from src.utils.config import CSV_DATASET_PATH, PARQUET_DATASET_PATH, PROCESSED_DATA_DIR, PREDICTIONS_OUTPUT_PATH

logger = logging.getLogger(__name__)


class DatasetLoader:
    """Manages merging, deduplication, and persistence of model datasets."""

    def __init__(self, csv_path: Path = CSV_DATASET_PATH, parquet_path: Path = PARQUET_DATASET_PATH):
        self.csv_path = csv_path
        self.parquet_path = parquet_path
        
        # Ensure target directory exists
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    def load_existing(self) -> pd.DataFrame:
        """Loads existing processed dataset if available, prioritizing Parquet then CSV."""
        if self.parquet_path.exists():
            try:
                df = pd.read_parquet(self.parquet_path)
                logger.info(f"Loaded existing Parquet dataset with {len(df)} records.")
                return df
            except Exception as e:
                logger.warning(f"Could not read Parquet dataset: {e}")

        if self.csv_path.exists():
            try:
                df = pd.read_csv(self.csv_path)
                logger.info(f"Loaded existing CSV dataset with {len(df)} records.")
                return df
            except Exception as e:
                logger.warning(f"Could not read CSV dataset: {e}")

        logger.info("No existing dataset found. Starting with empty dataset.")
        return pd.DataFrame()

    def merge_and_deduplicate(self, new_df: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merges new records with existing historical dataset and deduplicates by `model_id`.
        Prioritizes entries with higher downloads / likes.
        """
        if existing_df.empty:
            merged = new_df.copy()
        elif new_df.empty:
            merged = existing_df.copy()
        else:
            merged = pd.concat([existing_df, new_df], ignore_index=True)

        if merged.empty:
            return merged

        # Sort by downloads and last_modified descending so deduplication keeps newest/highest metrics
        if "last_modified" in merged.columns and "downloads" in merged.columns:
            merged = merged.sort_values(by=["downloads", "last_modified"], ascending=[False, False])

        # Deduplicate on model_id
        deduped = merged.drop_duplicates(subset=["model_id"], keep="first").reset_index(drop=True)
        
        # Re-sort by created_at descending (newest model releases at top)
        if "created_at" in deduped.columns:
            deduped = deduped.sort_values(by="created_at", ascending=False).reset_index(drop=True)

        logger.info(f"Deduplicated dataset from {len(merged)} total rows down to {len(deduped)} unique models.")
        return deduped

    def save_dataset(self, df: pd.DataFrame) -> Tuple[str, str]:
        """
        Saves the DataFrame to CSV and Parquet formats.
        
        Returns:
            Tuple[str, str]: Absolute paths to saved CSV and Parquet files
        """
        if df.empty:
            logger.warning("Attempted to save empty DataFrame. Skipping save.")
            return str(self.csv_path), str(self.parquet_path)

        # 1. Save CSV
        df.to_csv(self.csv_path, index=False)
        logger.info(f"Saved CSV dataset to {self.csv_path}")

        # 2. Save Parquet (compressed)
        try:
            df.to_parquet(self.parquet_path, index=False, engine="pyarrow", compression="snappy")
            logger.info(f"Saved Parquet dataset to {self.parquet_path}")
        except Exception as e:
            logger.error(f"Failed to save Parquet file: {e}")

        # 3. Export JSON payload for Dashboard consumption
        records = df.to_dict(orient="records")
        with open(PREDICTIONS_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        logger.info(f"Exported JSON snapshot to {PREDICTIONS_OUTPUT_PATH}")

        return str(self.csv_path), str(self.parquet_path)
