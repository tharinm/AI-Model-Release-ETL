"""
Extractor module to fetch model metadata from Hugging Face API.
"""
import os
import time
import logging
import requests
from typing import List, Dict, Any, Optional

from src.utils.config import HF_MODELS_API_URL, DEFAULT_FETCH_LIMIT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HuggingFaceExtractor:
    """Handles API extraction of AI/ML model metadata from Hugging Face."""

    def __init__(self, api_url: str = HF_MODELS_API_URL, token: Optional[str] = None):
        self.api_url = api_url
        self.token = token or os.getenv("HF_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def fetch_recent_models(self, limit: int = DEFAULT_FETCH_LIMIT, sort_by: str = "createdAt") -> List[Dict[str, Any]]:
        """
        Fetches recently created/modified models from Hugging Face.
        
        Args:
            limit (int): Number of models to retrieve (default: 500)
            sort_by (str): Property to sort by ('createdAt' or 'lastModified')
            
        Returns:
            List[Dict[str, Any]]: List of raw model metadata objects
        """
        params = {
            "limit": limit,
            "sort": sort_by,
            "direction": -1,
            "full": "true"
        }
        
        logger.info(f"Fetching top {limit} models sorted by {sort_by} from Hugging Face API...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.api_url,
                    headers=self.headers,
                    params=params,
                    timeout=20
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully retrieved {len(data)} raw model entries.")
                return data
            except requests.exceptions.RequestException as err:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {err}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error("Failed to fetch data from Hugging Face API after max retries.")
                    raise err

    def fetch_sample_models(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generates fallback/mock model data for testing or offline mode."""
        import random
        from datetime import datetime, timedelta, timezone

        pipeline_tags = ["text-generation", "image-classification", "text-to-image", "feature-extraction", "automatic-speech-recognition", "translation", "zero-shot-classification"]
        libraries = ["transformers", "diffusers", "timm", "vllm", "peft", "onnx"]
        authors = ["meta-llama", "mistralai", "google", "microsoft", "Qwen", "deepseek-ai", "stabilityai", "BAAI"]
        licenses = ["apache-2.0", "mit", "llama3", "other", "gpl-3.0", "cc-by-4.0"]

        mock_data = []
        now = datetime.now(timezone.utc)

        for i in range(count):
            author = random.choice(authors)
            m_name = f"model-{random.randint(100, 999)}-v{random.randint(1, 3)}"
            model_id = f"{author}/{m_name}"
            created_days_ago = random.randint(0, 60)
            created_dt = now - timedelta(days=created_days_ago, hours=random.randint(0, 23))
            
            downloads = random.randint(10, 500000)
            likes = int(downloads * random.uniform(0.005, 0.08))

            mock_data.append({
                "id": model_id,
                "author": author,
                "pipeline_tag": random.choice(pipeline_tags),
                "downloads": downloads,
                "likes": likes,
                "createdAt": created_dt.isoformat(),
                "lastModified": (created_dt + timedelta(days=random.randint(0, 5))).isoformat(),
                "library_name": random.choice(libraries),
                "tags": [
                    random.choice(pipeline_tags),
                    random.choice(libraries),
                    f"license:{random.choice(licenses)}",
                    "arxiv:2401.00000",
                    "en",
                    "dataset:common_crawl"
                ]
            })

        return mock_data
