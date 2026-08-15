"""
Training pipeline for model popularity predictor.
"""
import pickle
import logging
import pandas as pd
from typing import Dict, Any, Optional

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

from src.ml.feature_engineering import prepare_features, create_target_variable
from src.utils.config import MODEL_SAVE_PATH

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and serializes the Random Forest predictor model."""

    def __init__(self, model_save_path=MODEL_SAVE_PATH):
        self.model_save_path = model_save_path
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42,
            class_weight="balanced"
        )

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Trains the classifier on dataset features.
        
        Args:
            df (pd.DataFrame): Processed model metadata dataset
            
        Returns:
            Dict[str, Any]: Model performance metrics
        """
        if df.empty or len(df) < 10:
            logger.warning("Insufficient records (<10) to train model. Skipping training.")
            return {"status": "skipped", "reason": "insufficient_data"}

        X = prepare_features(df)
        y = create_target_variable(df)

        if y.nunique() < 2:
            logger.warning("Target variable has only one class. Adding synthetic balance for training.")
            y.iloc[: max(1, len(y) // 5)] = 1 - y.iloc[0]

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
        )

        # Fit Model
        self.model.fit(X_train, y_train)

        # Predictions & Metrics
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1] if hasattr(self.model, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        try:
            auc = roc_auc_score(y_test, y_prob)
        except Exception:
            auc = 0.5

        metrics = {
            "status": "success",
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "roc_auc": round(auc, 4),
            "sample_count": len(df)
        }

        logger.info(f"Model Training Complete. Metrics: {metrics}")

        # Save Artifact
        with open(self.model_save_path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Saved trained model to {self.model_save_path}")

        return metrics
