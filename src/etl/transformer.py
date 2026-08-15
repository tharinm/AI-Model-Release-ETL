"""
Transformer module for cleaning and enriching raw AI model metadata.
"""
import math
import logging
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Any

from src.utils.config import DATASET_COLUMNS

logger = logging.getLogger(__name__)


class ModelTransformer:
    """Cleans, normalizes, and enriches raw model metadata extracted from Hugging Face."""

    def __init__(self, reference_time: datetime = None):
        self.ref_time = reference_time or datetime.now(timezone.utc)

    def extract_license(self, tags: List[str]) -> str:
        """Extracts license information from model tags."""
        if not tags:
            return "unknown"
        for tag in tags:
            if isinstance(tag, str) and tag.startswith("license:"):
                return tag.replace("license:", "").strip()
        return "unknown"

    def extract_library(self, raw_item: Dict[str, Any], tags: List[str]) -> str:
        """Extracts deep learning framework/library."""
        if raw_item.get("library_name"):
            return str(raw_item.get("library_name")).strip()
        
        known_libs = ["transformers", "diffusers", "timm", "vllm", "peft", "onnx", "spacy", "flair", "fastai", "jax", "tensorflow", "pytorch"]
        if tags:
            for tag in tags:
                if isinstance(tag, str) and tag.lower() in known_libs:
                    return tag.lower()
        return "other"

    def parse_datetime(self, date_val: Any) -> str:
        """Standardizes timestamps to ISO 8601 strings."""
        if not date_val:
            return self.ref_time.isoformat()
        try:
            if isinstance(date_val, str):
                dt = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
            elif isinstance(date_val, (int, float)):
                dt = datetime.fromtimestamp(date_val / 1000.0, tz=timezone.utc)
            else:
                dt = date_val
            
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception:
            return self.ref_time.isoformat()

    def transform_record(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Transforms a single raw API item into a clean record."""
        model_id = str(raw.get("id") or raw.get("modelId") or "unknown/unknown").strip()
        
        # Author & Model name breakdown
        if "/" in model_id:
            author, model_name = model_id.split("/", 1)
        else:
            author = str(raw.get("author") or "community").strip()
            model_name = model_id

        pipeline_tag = str(raw.get("pipeline_tag") or "unspecified").strip()
        downloads = int(raw.get("downloads", 0) or 0)
        likes = int(raw.get("likes", 0) or 0)
        
        raw_tags = raw.get("tags") or []
        tags_list = [str(t).strip() for t in raw_tags if isinstance(t, str)]
        
        license_str = self.extract_license(tags_list)
        library_str = self.extract_library(raw, tags_list)
        
        created_str = self.parse_datetime(raw.get("createdAt"))
        modified_str = self.parse_datetime(raw.get("lastModified"))

        # Calculate Age in Days
        try:
            created_dt = datetime.fromisoformat(created_str)
            age_days = max(0.1, (self.ref_time - created_dt).total_seconds() / 86400.0)
        except Exception:
            age_days = 1.0

        # Ratios & Derived Metrics
        like_ratio = round(likes / max(1, downloads), 6)
        
        # Composite Popularity Score: weighted log scale of downloads & likes normalized by age
        log_dl = math.log1p(downloads)
        log_likes = math.log1p(likes)
        popularity_score = round((log_dl * 0.6 + log_likes * 0.4) / (math.log1p(age_days) ** 0.3 + 0.1), 4)

        return {
            "model_id": model_id,
            "author": author,
            "model_name": model_name,
            "model_type": pipeline_tag,
            "pipeline_tag": pipeline_tag,
            "downloads": downloads,
            "likes": likes,
            "created_at": created_str,
            "last_modified": modified_str,
            "library": library_str,
            "license": license_str,
            "tags": ", ".join(tags_list),
            "num_tags": len(tags_list),
            "age_days": round(age_days, 2),
            "like_to_download_ratio": like_ratio,
            "popularity_score": popularity_score
        }

    def transform_batch(self, raw_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Transforms a list of raw metadata dictionaries into a cleaned Pandas DataFrame.
        """
        transformed = [self.transform_record(item) for item in raw_list if item]
        df = pd.DataFrame(transformed)
        
        if df.empty:
            df = pd.DataFrame(columns=DATASET_COLUMNS)
        else:
            # Ensure proper schema ordering
            for col in DATASET_COLUMNS:
                if col not in df.columns:
                    df[col] = None
            df = df[DATASET_COLUMNS]

        logger.info(f"Transformed batch of {len(df)} records into standardized DataFrame.")
        return df
