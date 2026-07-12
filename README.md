# AI-Powered Task Management System

An intelligent task management system that uses NLP and machine learning to **automatically classify, prioritize and assign tasks** based on their descriptions, deadlines and user workloads.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NLTK](https://img.shields.io/badge/NLTK-NLP-154F5B)](https://www.nltk.org/)
[![Status](https://img.shields.io/badge/Status-Week%201%20Complete-success)](#)

---

## Problem Statement

Design and develop an intelligent task management system that leverages NLP and ML techniques to automatically classify, prioritize, and assign tasks to users based on their behavior, deadlines, and workloads.

## Project Structure

```
├── data/
│   ├── raw/
│   │   └── tasks.csv               # 8,110 task records (synthetic, seeded)
│   └── processed/
│       ├── tasks_clean.csv         # deduplicated, imputed, consistent labels
│       └── tasks_nlp.csv           # + preprocessed description text
├── docs/
│   └── DATASET.md                  # dataset documentation
├── notebooks/
│   ├── 01_EDA_Data_Cleaning.ipynb  # EDA, missing values, duplicates, visualizations
│   └── 02_NLP_Preprocessing.ipynb  # tokenization, stop words, lemmatization
├── scripts/
│   └── generate_task_dataset.py    # reproducible dataset generator (seed 42)
└── README.md
```

## Dataset

A **synthetic task management dataset** (8,110 rows → 8,000 after cleaning) modelled on Jira/Trello exports: free-text task descriptions, category, priority, status, deadlines, effort estimates and assignee workload fields. See [docs/DATASET.md](docs/DATASET.md) for full column descriptions and design rationale.

- **Week 2 classification target:** `category` (7 classes — Bug Fix, Feature, Testing, …)
- **Week 3 priority target:** `priority` (Low / Medium / High / Critical)
- **Workload balancing signals:** `assignee_open_tasks`, `assignee_experience_years`, `estimated_hours`

## Week 1 Deliverables (complete)

| Deliverable | Location |
|---|---|
| Task dataset collected + documented | `data/raw/tasks.csv`, `docs/DATASET.md` |
| EDA & data cleaning (missing values, duplicates, inconsistent labels, visualizations) | `notebooks/01_EDA_Data_Cleaning.ipynb` |
| Cleaned dataset | `data/processed/tasks_clean.csv` |
| NLP preprocessing (lowercase, punctuation removal, tokenization, stop words, lemmatization) | `notebooks/02_NLP_Preprocessing.ipynb` |
| Preprocessed dataset | `data/processed/tasks_nlp.csv` |

### Key EDA findings

- `category` is imbalanced (Bug Fix ~28% … Research ~5%) → stratified splits needed in Week 2
- `days_to_deadline` correlates strongly (negatively) with priority — the core Week 3 signal
- Effort estimates are log-normal shaped → median imputation used
- Workload/experience fields are independent of priority → reserved for assignment logic

## How to Run

```bash
pip install pandas numpy matplotlib seaborn nltk jupyter

# (optional) regenerate the dataset — deterministic, seed 42
python scripts/generate_task_dataset.py

# run the notebooks in order
jupyter notebook notebooks/01_EDA_Data_Cleaning.ipynb
jupyter notebook notebooks/02_NLP_Preprocessing.ipynb
```

All notebook paths are relative to the repository — no local absolute paths required.

## Roadmap

- **Week 1 — done:** dataset collection, EDA & cleaning, NLP preprocessing
- **Week 2:** TF-IDF / word-embedding features; task classification with Naive Bayes & SVM; evaluation (accuracy, precision, recall)
- **Week 3:** priority prediction (Random Forest / XGBoost), workload-balancing logic, GridSearchCV tuning
- **Week 4:** final models, dashboard mockup, performance report
