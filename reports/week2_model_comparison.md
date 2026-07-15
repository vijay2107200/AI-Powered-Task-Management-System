# Week 2 — Model Comparison Report

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Task:** classify `category` (7 classes) from preprocessed task descriptions

## Setup

- **Data:** `data/processed/tasks_nlp.csv` (8,000 tasks after Week 1 cleaning)
- **Split:** shared stratified 80/20 train/test split (`models/train_idx.joblib` / `test_idx.joblib`, seed 42) — every model below is evaluated on the **same 1,600 test tasks**
- **Features:** TF-IDF (unigram+bigram, `min_df=2`, `max_features=5000`, sublinear TF — chosen in `03_Feature_Extraction.ipynb`) and averaged Word2Vec document vectors (skip-gram, 100 dims, 20 epochs)
- **Tuning:** GridSearchCV, 5-fold stratified CV, macro-F1 scoring (NB: `alpha`; SVM: `C`, `class_weight="balanced"`)

## Results (shared test split)

| Model | Features | Accuracy | Macro Precision | Macro Recall | Macro F1 | Research Recall |
|---|---|---|---|---|---|---|
| Naive Bayes (α=0.01) | TF-IDF | 0.816 | 0.788 | 0.811 | **0.797** | 0.778 |
| **Linear SVM** | TF-IDF | 0.815 | **0.791** | **0.821** | 0.795 | **0.880** |
| Linear SVM | Word2Vec (avg) | 0.803 | 0.776 | 0.804 | 0.782 | 0.843 |

The Naive Bayes notebook (04) additionally compares its own unigram vs. bigram
vectorizers on the same split: bigram TF-IDF wins (accuracy 0.817, macro F1 0.797).

## Findings

1. **TF-IDF beats averaged Word2Vec** on this corpus. Task descriptions are short
   (~10 words), so averaging embeddings dilutes the few decisive words, while
   TF-IDF keeps them sharp.
2. **Naive Bayes and SVM tie on macro-F1** (0.797 vs 0.795 — inside noise), but the
   SVM's balanced class weights give it clearly better recall on the rare
   **Research** class (0.88 vs 0.78) and the best macro recall overall.
3. Remaining errors concentrate in genuinely ambiguous phrasings ("Update…",
   "Investigate…", "Prepare … for release") that plausibly belong to several
   categories, plus the dataset's ~5% label noise — irreducible from text alone.
4. Ceiling check: with 5% injected label noise, ~0.95 accuracy is the theoretical
   maximum; both models reach ~0.86 of the achievable range.

## Recommendation for Week 3

Carry the **Linear SVM on TF-IDF** forward (saved at `models/svm_tfidf.joblib`):
equal overall quality to NB with better worst-class behaviour, which matters when
routing every task type reliably. For priority prediction, combine the same TF-IDF
pipeline with `days_to_deadline` and `estimated_hours` — the strongest priority
signals from the Week 1 EDA — using Random Forest / XGBoost per the project plan.
