# Week 2 Plan — Feature Extraction & Task Classification

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Period:** 13 – 19 July 2026

## Goals (from the project brief)

1. Feature extraction using TF-IDF / word embeddings (Word2Vec, optionally BERT)
2. Task classification using Naive Bayes and SVM
3. Evaluation using accuracy, precision, recall
4. Mid-Project Review at the end of the week

## Task Allocation

### Member 1 — Coordination & Repository Management
- Review and merge pull requests; keep the folder structure organized
- Enforce the branch workflow (see below)
- Maintain README, progress notes and meeting notes
- Assemble the Mid-Project Review pack (`reports/mid_project_review.md`)

### Member 2 — Feature Extraction
- Build TF-IDF features from `description_processed` in `data/processed/tasks_nlp.csv`
  (compare unigrams vs. unigrams+bigrams; tune `min_df`, `max_features`)
- Train Word2Vec on task descriptions; produce averaged document vectors
  (optional: pretrained BERT sentence embeddings for comparison)
- Create the **shared stratified train/test split** (stratify on `category`, fixed
  `random_state`) and save it — both modelers must use this split
- Deliverables: `notebooks/03_Feature_Extraction.ipynb`, saved vectorizer/matrices in `models/`

### Member 3 — Naive Bayes Classifier
- Multinomial Naive Bayes on TF-IDF features predicting `category`
- Tune `alpha`; compare unigram vs. bigram features
- Report accuracy, precision, recall (per-class + macro) and a confusion matrix
- Deliverables: `notebooks/04_NaiveBayes_Classifier.ipynb`

### Member 4 — SVM Classifier & Combined Evaluation
- Linear SVM (`LinearSVC`, `class_weight="balanced"`) on TF-IDF and on Word2Vec vectors
- Tune `C`; compare feature sets
- Combined Naive Bayes vs. SVM evaluation on the shared test split, with a
  recommendation for Week 3
- Deliverables: `notebooks/05_SVM_Classifier.ipynb`, `reports/week2_model_comparison.md`

## Branch Workflow

| Branch | Owner | Purpose |
|---|---|---|
| `main` | Member 1 | Stable, review-ready state — changes land via PR only |
| `week2-features` | Member 2 | Feature extraction notebook + artifacts |
| `week2-naive-bayes` | Member 3 | Naive Bayes notebook |
| `week2-svm` | Member 4 | SVM notebook + comparison report |

Rules:
1. Work only on your own branch; open a PR to `main` when a deliverable is ready.
2. `week2-features` merges **first** (mid-week) — the classifiers depend on the shared split.
3. PRs need one review before merge; keep notebooks executed (outputs visible).
4. Do not commit large binary artifacts except the saved vectorizer/split under `models/`.

## Timeline

| Day | Milestone |
|---|---|
| Mon–Tue | Feature extraction ready; shared split saved and merged |
| Wed–Thu | Both classifiers trained and evaluated on the shared split |
| Fri | Comparison report; Mid-Project Review pack assembled |

## Mid-Project Review Checklist (end of Week 2)

- [x] Cleaned and preprocessed dataset (`data/processed/tasks_clean.csv`, `tasks_nlp.csv`)
- [x] EDA visualizations completed (`notebooks/01_EDA_Data_Cleaning.ipynb`)
- [x] Task classifier (Naive Bayes/SVM) trained and evaluated (notebooks 04 & 05)
- [x] Evaluation metrics (accuracy, precision, recall) documented (`reports/week2_model_comparison.md`)
