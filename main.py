"""
CLI Entry Point for AI Model Release ETL & Popularity Prediction Pipeline.
"""
import sys
import argparse
import logging
import pandas as pd

from src.etl.extractor import HuggingFaceExtractor
from src.etl.transformer import ModelTransformer
from src.etl.loader import DatasetLoader
from src.ml.train import ModelTrainer
from src.ml.predict import PopularityPredictor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIModelTracker")


def run_pipeline(limit: int = 500, use_mock: bool = False, train: bool = True):
    """Executes full ETL, training, and prediction pipeline."""
    logger.info("=== Starting AI Model Release ETL Pipeline ===")

    # 1. Extraction
    extractor = HuggingFaceExtractor()
    if use_mock:
        logger.info("Using mock model metadata generator...")
        raw_data = extractor.fetch_sample_models(count=limit)
    else:
        try:
            raw_data = extractor.fetch_top_models(limit=limit)
        except Exception as e:
            logger.warning(f"Failed to fetch live API data ({e}). Falling back to sample model generator.")
            raw_data = extractor.fetch_sample_models(count=limit)

    # 2. Transformation
    transformer = ModelTransformer()
    new_df = transformer.transform_batch(raw_data)

    # 3. Loading & Merging
    loader = DatasetLoader()
    existing_df = loader.load_existing()
    merged_df = loader.merge_and_deduplicate(new_df, existing_df)

    # 4. ML Prediction & Training
    if train or not loader.parquet_path.exists():
        logger.info("=== Training ML Popularity Predictor ===")
        trainer = ModelTrainer()
        trainer.train(merged_df)

    predictor = PopularityPredictor()
    final_df = predictor.predict(merged_df)

    # 5. Save Output
    csv_path, parquet_path = loader.save_dataset(final_df)
    
    logger.info("=== ETL Pipeline Execution Summary ===")
    logger.info(f"Total Unique Models Processed: {len(final_df)}")
    logger.info(f"Top 5 Popular Models:\n{final_df[['model_id', 'downloads', 'likes', 'popularity_probability']].head(5)}")
    logger.info(f"CSV Path: {csv_path}")
    logger.info(f"Parquet Path: {parquet_path}")
    logger.info("=== Pipeline Completed Successfully ===")


def main():
    parser = argparse.ArgumentParser(description="AI Model Release ETL & Popularity Prediction Pipeline")
    parser.add_argument("--run-etl", action="store_true", help="Execute ETL data extraction & dataset updating")
    parser.add_argument("--train-ml", action="store_true", help="Train ML popularity model")
    parser.add_argument("--predict", action="store_true", help="Run popularity predictions on dataset")
    parser.add_argument("--use-mock", action="store_true", help="Use fallback mock data for testing")
    parser.add_argument("--limit", type=int, default=500, help="Number of models to fetch from Hugging Face")

    args = parser.parse_args()

    # Default to full pipeline if no flags specified
    if not any([args.run_etl, args.train_ml, args.predict]):
        run_pipeline(limit=args.limit, use_mock=args.use_mock, train=True)
        return

    if args.run_etl:
        run_pipeline(limit=args.limit, use_mock=args.use_mock, train=args.train_ml)
    elif args.train_ml:
        loader = DatasetLoader()
        df = loader.load_existing()
        trainer = ModelTrainer()
        trainer.train(df)
    elif args.predict:
        loader = DatasetLoader()
        df = loader.load_existing()
        predictor = PopularityPredictor()
        out_df = predictor.predict(df)
        loader.save_dataset(out_df)


if __name__ == "__main__":
    main()
