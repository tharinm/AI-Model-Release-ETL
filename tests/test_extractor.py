"""
Unit tests for HuggingFaceExtractor module.
"""
import unittest
from src.etl.extractor import HuggingFaceExtractor


class TestExtractor(unittest.TestCase):

    def test_fetch_sample_models(self):
        extractor = HuggingFaceExtractor()
        sample_data = extractor.fetch_sample_models(count=25)
        
        self.assertEqual(len(sample_data), 25)
        self.assertIn("id", sample_data[0])
        self.assertIn("downloads", sample_data[0])
        self.assertIn("likes", sample_data[0])
        self.assertIn("createdAt", sample_data[0])
        self.assertIsInstance(sample_data[0]["tags"], list)


if __name__ == "__main__":
    unittest.main()
