# Week 3 Progress Summary — Priority Prediction & Workload Balancing

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Period:** 20 – 26 July 2026

## 1. Deliverable Status

| Deliverable (from `docs/WEEK3_PLAN.md`) | Owner | Status | Location |
|---|---|---|---|
| Priority feature matrix (shared) | Member 2 | ⏳ Pending | `models/` |
| Random Forest priority model (GridSearchCV) | Member 2 | ⏳ Pending | `notebooks/06_Priority_RandomForest.ipynb` |
| XGBoost priority model (GridSearchCV) | Member 3 | ⏳ Pending | `notebooks/07_Priority_XGBoost.ipynb` |
| RF vs. XGBoost comparison + Week 4 recommendation | Member 3 | ⏳ Pending | `reports/week3_priority_comparison.md` |
| Workload balancer + simulation | Member 4 | ⏳ Pending | `notebooks/08_Workload_Balancing.ipynb`, `scripts/workload_balancer.py` |
| End-to-end integration check | Member 1 | ⏳ Pending | this report, section 3 |

## 2. Model Results (shared stratified test split)

*(filled in as PRs merge)*

| Model | Features | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---|---|---|---|---|
| Random Forest | TF-IDF + numeric | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| XGBoost | TF-IDF + numeric | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

Reference baseline from Week 2 (category classification, same split discipline):
Linear SVM on TF-IDF — accuracy 0.815, macro F1 0.795.

## 3. Integration Check (end of week)

Pipeline to verify on a handful of unseen example tasks:

1. Raw task description → Week 1 preprocessing → shared TF-IDF vectorizer
2. → **priority model** predicts Low / Medium / High / Critical
3. → **workload balancer** scores the 25 users and suggests an assignee

- [ ] Steps run end-to-end from the committed artifacts in `models/` and `scripts/`
- [ ] Suggested assignees respect workload and experience constraints
- [ ] Example walkthrough recorded here for the Week 4 dashboard/demo

## 4. Risks / Notes

- `priority` is milder in imbalance than `category` (Critical ~17%), but macro
  metrics and stratified splits remain the standard
- XGBoost requires `pip install xgboost` (Python ≤3.13 venv, same as gensim)
- Week 3 branches are created fresh off the cleaned history — **re-clone, don't
  pull into old clones**
