"""
Unit tests for ModelTransformer module.
"""
import unittest
import pandas as pd
from datetime import datetime, timezone
from src.etl.transformer import ModelTransformer


class TestTransformer(unittest.TestCase):

    def test_transform_record(self):
        transformer = ModelTransformer(reference_time=datetime(2026, 8, 15, tzinfo=timezone.utc))
        raw_item = {
            "id": "meta-llama/Llama-3-8B",
            "author": "meta-llama",
            "pipeline_tag": "text-generation",
            "downloads": 10000,
            "likes": 500,
            "createdAt": "2026-08-01T00:00:00Z",
            "lastModified": "2026-08-05T00:00:00Z",
            "library_name": "transformers",
            "tags": ["text-generation", "transformers", "license:llama3", "en"]
        }
        
        transformed = transformer.transform_record(raw_item)
        
        self.assertEqual(transformed["model_id"], "meta-llama/Llama-3-8B")
        self.assertEqual(transformed["author"], "meta-llama")
        self.assertEqual(transformed["model_name"], "Llama-3-8B")
        self.assertEqual(transformed["downloads"], 10000)
        self.assertEqual(transformed["likes"], 500)
        self.assertEqual(transformed["license"], "llama3")
        self.assertEqual(transformed["library"], "transformers")
        self.assertEqual(transformed["like_to_download_ratio"], 0.05)
        self.assertGreater(transformed["age_days"], 10.0)

    def test_transform_batch(self):
        transformer = ModelTransformer()
        raw_batch = [
            {
                "id": "author1/model1",
                "pipeline_tag": "text-to-image",
                "downloads": 50,
                "likes": 5,
                "tags": ["license:mit"]
            },
            {
                "id": "author2/model2",
                "pipeline_tag": "translation",
                "downloads": 200,
                "likes": 20,
                "tags": ["license:apache-2.0"]
            }
        ]
        df = transformer.transform_batch(raw_batch)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("popularity_score", df.columns)
        self.assertEqual(df.loc[0, "license"], "mit")


if __name__ == "__main__":
    unittest.main()
