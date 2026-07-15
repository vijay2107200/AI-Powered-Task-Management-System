# Mid-Project Review — AI-Powered Task Management System

**Prepared by:** Vijayasiva
**Review point:** End of Week 2

## 1. Deliverable Status

| Deliverable (from project brief) | Status | Location |
|---|---|---|
| Cleaned and preprocessed dataset | ✅ Done | `data/processed/tasks_clean.csv`, `data/processed/tasks_nlp.csv` |
| EDA visualizations completed | ✅ Done | `notebooks/01_EDA_Data_Cleaning.ipynb` |
| Task classifier (Naive Bayes/SVM) trained and evaluated | ✅ Done | `notebooks/04_NaiveBayes_Classifier.ipynb`, `notebooks/05_SVM_Classifier.ipynb` |

## 2. Week 1 Summary

- Collected a reproducible task management dataset (8,110 tasks, Jira/Trello-style
  fields with free-text descriptions) — documented in `docs/DATASET.md`
- EDA: category/priority/status distributions, correlation analysis, deadline–priority
  relationship identified as the core Week 3 signal
- Cleaning: 110 duplicates dropped, labels normalized, effort fields median-imputed
- NLP preprocessing: lowercase → punctuation removal → tokenization → stop-word
  removal → lemmatization, verified clean; output ready for feature extraction

## 3. Week 2 Results

### Feature extraction (`notebooks/03_Feature_Extraction.ipynb`)
- TF-IDF configuration chosen: **unigram+bigram, `min_df=2`, `max_features=5000`,
  sublinear TF** (best balance of vocabulary size vs. signal across 4 tested configs)
- Word2Vec: skip-gram, 100 dimensions, 20 epochs, averaged into document vectors
- Shared stratified 80/20 split saved to `models/` and used by **both** classifiers

### Model evaluation (shared stratified test split, 1,600 tasks)

| Model | Features | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---|---|---|---|---|
| Naive Bayes (α=0.01) | TF-IDF | 0.816 | 0.788 | 0.811 | 0.797 |
| **Linear SVM** | TF-IDF | 0.815 | 0.791 | 0.821 | 0.795 |
| Linear SVM | Word2Vec (avg) | 0.803 | 0.776 | 0.804 | 0.782 |

Full analysis: `reports/week2_model_comparison.md`

### Recommendation for Week 3
**Linear SVM on TF-IDF** (`models/svm_tfidf.joblib`) — ties Naive Bayes on macro-F1
but with clearly better recall on the rarest class (Research: 0.88 vs 0.78), so it
degrades least across all task types. Week 3 priority prediction will combine this
TF-IDF pipeline with `days_to_deadline` and `estimated_hours` using Random
Forest / XGBoost.

## 4. Risks / Notes

- `category` is imbalanced (Research ~7%) — handled with stratified splits, balanced
  class weights and macro-averaged metrics throughout
- The dataset contains ~5% label noise by design (realism), which caps achievable
  accuracy around 0.95; current models reach ~0.82
- All notebooks run top-to-bottom with repo-relative paths (`pip install -r` style
  setup documented in the README)
