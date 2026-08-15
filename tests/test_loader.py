"""
Unit tests for DatasetLoader module.
"""
import unittest
import tempfile
import pandas as pd
from pathlib import Path
from src.etl.loader import DatasetLoader


class TestLoader(unittest.TestCase):

    def test_merge_and_deduplicate(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            loader = DatasetLoader(
                csv_path=tmp_path / "test.csv",
                parquet_path=tmp_path / "test.parquet"
            )

            df_old = pd.DataFrame([
                {"model_id": "meta/llama-1", "downloads": 100, "likes": 10, "last_modified": "2026-08-01T00:00:00Z", "created_at": "2026-08-01T00:00:00Z"},
                {"model_id": "google/gemma-1", "downloads": 50, "likes": 5, "last_modified": "2026-08-01T00:00:00Z", "created_at": "2026-08-01T00:00:00Z"}
            ])

            df_new = pd.DataFrame([
                {"model_id": "meta/llama-1", "downloads": 500, "likes": 50, "last_modified": "2026-08-10T00:00:00Z", "created_at": "2026-08-01T00:00:00Z"},
                {"model_id": "mistral/mistral-7b", "downloads": 1000, "likes": 100, "last_modified": "2026-08-10T00:00:00Z", "created_at": "2026-08-05T00:00:00Z"}
            ])

            deduped = loader.merge_and_deduplicate(df_new, df_old)

            self.assertEqual(len(deduped), 3)
            llama_entry = deduped[deduped["model_id"] == "meta/llama-1"].iloc[0]
            self.assertEqual(llama_entry["downloads"], 500)

    def test_save_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            csv_file = tmp_path / "out.csv"
            parquet_file = tmp_path / "out.parquet"
            loader = DatasetLoader(csv_path=csv_file, parquet_path=parquet_file)

            df = pd.DataFrame([
                {"model_id": "org/model-a", "downloads": 10, "likes": 1, "created_at": "2026-08-01T00:00:00Z"}
            ])

            c_path, p_path = loader.save_dataset(df)

            self.assertTrue(Path(c_path).exists())
            self.assertTrue(Path(p_path).exists())


if __name__ == "__main__":
    unittest.main()
