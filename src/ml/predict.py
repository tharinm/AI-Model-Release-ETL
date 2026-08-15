"""
Inference engine for predicting popularity of newly released AI models.
"""
import pickle
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Any

from src.ml.feature_engineering import prepare_features
from src.utils.config import MODEL_SAVE_PATH

logger = logging.getLogger(__name__)


class PopularityPredictor:
    """Predicts popularity probabilities for new model releases."""

    def __init__(self, model_path: Path = MODEL_SAVE_PATH):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self) -> Optional[Any]:
        """Loads serialized trained model artifact if available."""
        if self.model_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    model = pickle.load(f)
                logger.info(f"Successfully loaded ML predictor model from {self.model_path}")
                return model
            except Exception as e:
                logger.warning(f"Could not load ML model: {e}")
        return None

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds `popularity_probability` and `is_predicted_popular` columns to the DataFrame.
        """
        if df.empty:
            return df

        res_df = df.copy()

        if self.model is not None:
            try:
                X = prepare_features(res_df)
                probs = self.model.predict_proba(X)[:, 1]
                res_df["popularity_probability"] = np.round(probs, 4)
                res_df["is_predicted_popular"] = (probs >= 0.5).astype(int)
                logger.info("Computed ML model popularity probabilities successfully.")
                return res_df
            except Exception as e:
                logger.warning(f"Error during ML prediction, falling back to heuristic score: {e}")

        # Heuristic Fallback based on normalized popularity score
        if "popularity_score" in res_df.columns:
            scores = res_df["popularity_score"].fillna(0.0)
            max_s = max(1.0, scores.max())
            probs = (scores / max_s).clip(0.0, 1.0)
            res_df["popularity_probability"] = np.round(probs, 4)
            res_df["is_predicted_popular"] = (probs >= 0.6).astype(int)
        else:
            res_df["popularity_probability"] = 0.5
            res_df["is_predicted_popular"] = 0

        return res_df
