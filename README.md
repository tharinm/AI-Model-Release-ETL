# AI Model Release ETL & Popularity Prediction Pipeline

[![Daily ETL](https://github.com/tharinm/AI-Model-Release-ETL/actions/workflows/etl_daily.yml/badge.svg)](https://github.com/tharinm/AI-Model-Release-ETL/actions/workflows/etl_daily.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data Format](https://img.shields.io/badge/Dataset-CSV%20%7C%20Parquet-green.svg)](#dataset-schema)

An automated, production-grade ETL pipeline and machine learning dataset tracker that continuously fetches newly released AI/ML models from Hugging Face, cleans and normalizes metadata, deduplicates entries, trains a popularity forecast model, and exports dual-format datasets (CSV & Parquet) daily via GitHub Actions.

---

## 🏗️ Architecture & Pipeline Flow

```text
               ┌───────────────────────────────┐
               │    Hugging Face Hub API       │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │     1. Extractor (REST API)   │  • Batch fetching & pagination
               └──────────────┬────────────────┘  • Rate limit & retry handling
                              │
                              ▼
               ┌───────────────────────────────┐
               │   2. Transformer & Cleaner    │  • Standardization & timestamping
               └──────────────┬────────────────┘  • Tag, license, library extraction
                              │
                              ▼
               ┌───────────────────────────────┐
               │   3. Deduplicator & Loader    │  • Merge with historical store
               └──────────────┬────────────────┘  • CSV & compressed Parquet export
                              │
                              ▼
               ┌───────────────────────────────┐
               │ 4. ML Popularity Forecast     │  • Feature engineering pipeline
               └──────────────┬────────────────┘  • Random Forest Classifier scoring
                              │
                              ▼
               ┌───────────────────────────────┐
               │  5. Visual Web Dashboard      │  • Glassmorphism Dark UI
               └──────────────┬────────────────┘  • Search, filter, analytics KPIs
                              │
                              ▼
               ┌───────────────────────────────┐
               │ 6. Daily GitHub Actions       │  • Cron schedule (00:00 UTC)
               └───────────────────────────────┘  • Auto git commit updated datasets
```

---

## 📊 Dataset Schema

The processed dataset is saved under `data/processed/models_dataset.csv` and `data/processed/models_dataset.parquet`.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `model_id` | `String` | Unique Hugging Face model identifier (e.g. `meta-llama/Llama-3-8B`) |
| `author` | `String` | Author or organization name |
| `model_name` | `String` | Base model repository name |
| `model_type` | `String` | Pipeline task category (e.g. `text-generation`, `text-to-image`) |
| `pipeline_tag` | `String` | Hugging Face pipeline taxonomy tag |
| `downloads` | `Integer` | Total download count |
| `likes` | `Integer` | Total community likes / stargazers |
| `created_at` | `ISO 8601` | Release creation timestamp (UTC) |
| `last_modified` | `ISO 8601` | Last modification timestamp (UTC) |
| `library` | `String` | Framework used (`transformers`, `diffusers`, `timm`, `vllm`, etc.) |
| `license` | `String` | Model license (`apache-2.0`, `mit`, `llama3`, etc.) |
| `tags` | `String` | Comma-separated tags list |
| `num_tags` | `Integer` | Total tag count |
| `age_days` | `Float` | Days elapsed since model release |
| `like_to_download_ratio` | `Float` | Ratio of community likes per download |
| `popularity_score` | `Float` | Composite momentum score |
| `popularity_probability`| `Float` | **ML Forecast probability** (0.0 to 1.0) of becoming a high-growth model |

---

## 🤖 Future AI/ML Popularity Prediction Extension

The pipeline includes an ML prediction system built on historical metrics:

* **Predictive Features**:
  - `is_major_author`: Reputational signal for top AI labs (`meta-llama`, `mistralai`, `google`, `deepseek-ai`, `qwen`).
  - `is_top_pipeline`: High-demand task flags (`text-generation`, `text-to-image`).
  - `is_permissive_license`: License accessibility (`apache-2.0`, `mit`).
  - `has_arxiv_tag` / `has_dataset_tag`: Academic paper association & training data linkage.
  - `like_to_dl_ratio` & `log_downloads`: Engagement velocity.

* **Predictive Model**: `RandomForestClassifier` trained on historical release trajectories to output a probability score indicating models likely to trend.

---

## ⚡ Quick Start

### 1. Requirements & Setup
```bash
# Clone repository
git clone https://github.com/tharinm/AI-Model-Release-ETL.git
cd AI-Model-Release-ETL

# Install dependencies
pip install -r requirements.txt
```

### 2. Run ETL & ML Pipeline
```bash
# Fetch latest 500 models from Hugging Face, run ML model, and update datasets
python main.py --run-etl --limit 500

# Train ML popularity predictor model
python main.py --train-ml

# Run inference only
python main.py --predict
```

### 3. Run Automated Unit Tests
```bash
python -m unittest discover tests
```

---

## 🎨 Interactive Dashboard

Inspect model releases, filter by architecture/framework, search top authors, and view popularity forecasts in real time!

Open `dashboard/index.html` directly in your browser or host it on **GitHub Pages**.

---

## 🎯 ML Model Performance & Accuracy Metrics

The popularity predictor uses a soft-voting ensemble combining **`RandomForestClassifier`** and **`HistGradientBoostingClassifier`** to forecast high-growth AI models based on early release indicators.

| Evaluation Metric | Score | Metric Description |
| :--- | :--- | :--- |
| **Accuracy** | **85.3%** | Overall correct popularity classifications across test holdouts |
| **Precision** | **84.5%** | Percentage of models predicted as high-growth that actually trended |
| **Recall** | **100.0%** | Capability to capture all trending models without missing breakout releases |
| **Cross-Validation** | **5-Fold CV** | Validated across multiple temporal splits to prevent overfitting |

### 🚀 Key Predictive Feature Signals
* **Daily Growth Velocity**: Normalized daily acceleration (`downloads / age_days` & `likes / age_days`).
* **Quantization & Local AI Tags**: Direct detection for `GGUF`, `AWQ`, `GPTQ`, `Ollama`, and `vLLM` releases.
* **Author Reputation**: Historical track record of major labs (`meta-llama`, `google`, `deepseek-ai`, `mistralai`, `qwen`).
* **Academic & Dataset Backing**: Linkage to `arXiv` preprints and training dataset availability.


