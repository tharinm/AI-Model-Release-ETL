"""
Optimized feature engineering module for AI model popularity prediction.
"""
import numpy as np
import pandas as pd
from typing import Tuple

MAJOR_AUTHORS = {
    "meta-llama", "mistralai", "google", "microsoft", "qwen",
    "deepseek-ai", "stabilityai", "baai", "nomic-ai", "tiiuae",
    "unsloth", "huggingface", "facebook", "openai"
}

TOP_PIPELINES = {
    "text-generation", "text-to-image", "image-classification",
    "automatic-speech-recognition", "feature-extraction", "translation",
    "depth-estimation", "text-to-speech", "image-to-text"
}

QUANT_KEYWORDS = ["gguf", "awq", "gptq", "quantized", "fp16", "int4", "int8", "bnb", "ollama", "vllm"]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts high-signal predictive features from model metadata.
    """
    features = pd.DataFrame(index=df.index)

    # 1. Author Reputational Signals
    author_clean = df["author"].astype(str).str.lower()
    features["is_major_author"] = author_clean.isin(MAJOR_AUTHORS).astype(int)

    # 2. Pipeline & Architecture Categorical Signals
    pipeline_clean = df["pipeline_tag"].astype(str).str.lower()
    features["is_text_gen"] = (pipeline_clean == "text-generation").astype(int)
    features["is_image_gen"] = (pipeline_clean == "text-to-image").astype(int)
    features["is_top_pipeline"] = pipeline_clean.isin(TOP_PIPELINES).astype(int)

    # 3. Model Name Signals & Quantization (GGUF / Ollama / AWQ)
    model_id_clean = df["model_id"].astype(str).str.lower()
    features["is_quantized"] = model_id_clean.apply(
        lambda name: int(any(kw in name for kw in QUANT_KEYWORDS))
    )
    features["is_gguf"] = model_id_clean.str.contains("gguf").astype(int)
    features["is_instruct"] = model_id_clean.apply(
        lambda name: int("instruct" in name or "chat" in name or "it" in name)
    )

    # 4. Framework & License Signals
    library_clean = df["library"].astype(str).str.lower()
    features["is_transformers"] = (library_clean == "transformers").astype(int)
    features["is_diffusers"] = (library_clean == "diffusers").astype(int)

    license_clean = df["license"].astype(str).str.lower()
    features["is_permissive_license"] = license_clean.isin(["apache-2.0", "mit"]).astype(int)

    # 5. Tag Density & Metadata Signals
    features["num_tags"] = df["num_tags"].fillna(0).astype(int)
    tags_str = df["tags"].astype(str).str.lower()
    features["has_arxiv_tag"] = tags_str.str.contains("arxiv").astype(int)
    features["has_dataset_tag"] = tags_str.str.contains("dataset").astype(int)
    features["has_base_model_tag"] = tags_str.str.contains("base_model").astype(int)

    # 6. Age & Velocity Features (Normalized Daily Growth Rate)
    age = df["age_days"].fillna(1.0).clip(lower=0.05)
    downloads = df["downloads"].fillna(0).clip(lower=0)
    likes = df["likes"].fillna(0).clip(lower=0)

    features["age_days"] = age
    features["log_age"] = np.log1p(age)
    
    # Velocity: Downloads & Likes per day
    features["downloads_per_day"] = np.log1p(downloads / age)
    features["likes_per_day"] = np.log1p(likes / age)

    # 7. Metric Ratios
    features["log_downloads"] = np.log1p(downloads)
    features["log_likes"] = np.log1p(likes)
    features["like_to_dl_ratio"] = df["like_to_download_ratio"].fillna(0.0)

    return features


def create_target_variable(df: pd.DataFrame) -> pd.Series:
    """
    Defines high-velocity popularity target variable:
    Model is popular if downloads per day or likes per day exceed top 30% threshold.
    """
    if df.empty or len(df) < 5:
        return (df["downloads"] > 200).astype(int)

    age = df["age_days"].fillna(1.0).clip(lower=0.1)
    dl_speed = df["downloads"] / age
    like_speed = df["likes"] / age

    dl_thresh = dl_speed.quantile(0.70)
    like_thresh = like_speed.quantile(0.70)

    is_popular = ((dl_speed >= dl_thresh) | (like_speed >= like_thresh)).astype(int)
    return is_popular
