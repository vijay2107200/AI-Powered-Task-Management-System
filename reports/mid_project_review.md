# Mid-Project Review — AI-Powered Task Management System

**Prepared by:** Vijayasiva
**Review point:** End of Week 2

## 1. Deliverable Status

| Deliverable (from project brief) | Status | Location |
|---|---|---|
| Cleaned and preprocessed dataset | ✅ Done | `data/processed/tasks_clean.csv`, `data/processed/tasks_nlp.csv` |
| EDA visualizations completed | ✅ Done | `notebooks/01_EDA_Data_Cleaning.ipynb` |
| Task classifier (Naive Bayes/SVM) trained and evaluated | ⏳ In progress | `notebooks/04_NaiveBayes_Classifier.ipynb`, `notebooks/05_SVM_Classifier.ipynb` |

## 2. Week 1 Summary

- Collected a reproducible task management dataset (8,110 tasks, Jira/Trello-style
  fields with free-text descriptions) — documented in `docs/DATASET.md`
- EDA: category/priority/status distributions, correlation analysis, deadline–priority
  relationship identified as the core Week 3 signal
- Cleaning: 110 duplicates dropped, labels normalized, effort fields median-imputed
- NLP preprocessing: lowercase → punctuation removal → tokenization → stop-word
  removal → lemmatization, verified clean; output ready for feature extraction

## 3. Week 2 Results

*(to be filled as PRs merge)*

### Feature extraction
- TF-IDF configuration chosen: _TBD_
- Word2Vec / embedding comparison: _TBD_

### Model evaluation (shared stratified test split)

| Model | Features | Accuracy | Macro Precision | Macro Recall |
|---|---|---|---|---|
| Naive Bayes | TF-IDF | _TBD_ | _TBD_ | _TBD_ |
| Linear SVM | TF-IDF | _TBD_ | _TBD_ | _TBD_ |
| Linear SVM | Word2Vec | _TBD_ | _TBD_ | _TBD_ |

### Recommendation for Week 3
_TBD after comparison._

## 4. Risks / Notes

- `category` is imbalanced (Research ~5%) — all metrics reported per-class and macro,
  splits stratified
- Priority prediction (Week 3) will reuse the same feature pipeline plus
  `days_to_deadline` and `estimated_hours`
