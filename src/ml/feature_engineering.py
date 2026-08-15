"""
Feature engineering module for AI model popularity prediction.
"""
import numpy as np
import pandas as pd
from typing import Tuple, List

MAJOR_AUTHORS = {
    "meta-llama", "mistralai", "google", "microsoft", "qwen",
    "deepseek-ai", "stabilityai", "baai", "nomic-ai", "tiiuae"
}

TOP_PIPELINES = {
    "text-generation", "text-to-image", "image-classification",
    "automatic-speech-recognition", "feature-extraction", "translation"
}


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts predictive tabular features from model metadata.
    """
    features = pd.DataFrame(index=df.index)

    # 1. Author Reputational Signals
    author_clean = df["author"].astype(str).str.lower()
    features["is_major_author"] = author_clean.isin(MAJOR_AUTHORS).astype(int)

    # 2. Category / Pipeline Tag One-Hot Signals
    pipeline_clean = df["pipeline_tag"].astype(str).str.lower()
    features["is_text_gen"] = (pipeline_clean == "text-generation").astype(int)
    features["is_image_gen"] = (pipeline_clean == "text-to-image").astype(int)
    features["is_top_pipeline"] = pipeline_clean.isin(TOP_PIPELINES).astype(int)

    # 3. Framework & License Signals
    library_clean = df["library"].astype(str).str.lower()
    features["is_transformers"] = (library_clean == "transformers").astype(int)
    features["is_diffusers"] = (library_clean == "diffusers").astype(int)

    license_clean = df["license"].astype(str).str.lower()
    features["is_permissive_license"] = license_clean.isin(["apache-2.0", "mit"]).astype(int)

    # 4. Content Metadata Signals
    features["num_tags"] = df["num_tags"].fillna(0).astype(int)
    features["has_arxiv_tag"] = df["tags"].astype(str).str.contains("arxiv", case=False).astype(int)
    features["has_dataset_tag"] = df["tags"].astype(str).str.contains("dataset", case=False).astype(int)

    # 5. Age & Velocity Features
    age = df["age_days"].fillna(1.0).clip(lower=0.1)
    features["age_days"] = age
    features["log_age"] = np.log1p(age)

    # 6. Metric Log Transformation
    downloads = df["downloads"].fillna(0).clip(lower=0)
    likes = df["likes"].fillna(0).clip(lower=0)
    
    features["log_downloads"] = np.log1p(downloads)
    features["log_likes"] = np.log1p(likes)
    features["like_to_dl_ratio"] = df["like_to_download_ratio"].fillna(0.0)

    return features


def create_target_variable(df: pd.DataFrame, quantile_threshold: float = 0.75) -> pd.Series:
    """
    Creates a binary target label `is_popular` (1 if in top quantile of downloads/likes, 0 otherwise).
    """
    if df.empty or len(df) < 5:
        # Fallback dummy threshold
        return (df["downloads"] > 500).astype(int)
    
    dl_threshold = df["downloads"].quantile(quantile_threshold)
    like_threshold = df["likes"].quantile(quantile_threshold)
    
    # Popular if downloads or likes exceed top 25th percentile
    is_popular = ((df["downloads"] >= dl_threshold) | (df["likes"] >= like_threshold)).astype(int)
    return is_popular
