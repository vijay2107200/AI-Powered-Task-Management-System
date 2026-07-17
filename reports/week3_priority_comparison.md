# Week 3 — Priority Prediction: Random Forest vs. XGBoost

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Task:** predict `priority` (Low / Medium / High / Critical) from task text + numeric features

## Setup

- **Features (identical for both models):** shared TF-IDF matrix from `models/` +
  `days_to_deadline`, `estimated_hours`, `story_points` + one-hot `category`
  (assembled in `notebooks/07_Priority_XGBoost.ipynb`, saved as
  `models/priority_X_train.joblib` / `priority_X_test.joblib` for reuse)
- **Split:** the shared stratified 80/20 split (`train_idx`/`test_idx`, seed 42) —
  same 1,600 test tasks used throughout Weeks 2–3
- **Tuning:** GridSearchCV, 5-fold stratified CV, macro-F1 scoring
  - Random Forest (notebook 06): `n_estimators`, `max_depth`, `min_samples_leaf`,
    `class_weight` → best: `n_estimators=100`, `max_depth=None`, `min_samples_leaf=4`
  - XGBoost (notebook 07): `n_estimators`, `max_depth`, `learning_rate`, `subsample`
    → best: `n_estimators=150`, `max_depth=4`, `learning_rate=0.1`, `subsample=0.8`

> **Note on comparability:** notebook 06's committed run used pre-update local
> artifacts, so its Random Forest was re-fit in notebook 07 with the same tuned
> hyperparameters on the current shared features. The table below is therefore a
> true like-for-like comparison.

## Results (shared test split, 1,600 tasks)

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Critical Recall |
|---|---|---|---|---|---|
| Random Forest (nb06 params) | 0.559 | 0.557 | 0.556 | 0.538 | 0.793 |
| **XGBoost (tuned)** | **0.631** | **0.644** | **0.636** | **0.638** | **0.819** |

## Findings

1. **XGBoost beats Random Forest on every metric** — +7 points accuracy and +10
   points macro F1. Gradient boosting extracts more from the mixed sparse-text +
   numeric feature space, and the shallow tuned trees (`max_depth=4`,
   `learning_rate=0.1`) generalize better than the forest's deep trees.
2. **Both models agree on what matters:** `days_to_deadline` is by far the top
   feature (importance ≈ 0.26 in RF, dominant in XGBoost too), followed by
   `estimated_hours` and the Bug Fix / Deployment category flags plus urgency
   tokens (`urgent`, `asap`) — exactly the signals the Week 1 EDA predicted.
3. **Critical tasks are caught well** (recall 0.82 for XGBoost) — the most
   important class operationally; most residual confusion is between adjacent
   classes (Medium ↔ Low / High), which is expected since priority was generated
   from continuous deadline/effort scores with noise.
4. Priority scores sit below Week 2's category-classification results (~0.82
   accuracy) because priority is intrinsically noisier — it derives from
   thresholded continuous signals plus ~5% label noise, so class boundaries
   genuinely overlap.

## Recommendation for Week 4

Carry **XGBoost** (`models/priority_xgb_model.joblib`) forward as the priority
model. Final Week 4 pipeline per task: description → Week 1 preprocessing →
shared TF-IDF → **SVM predicts category** (Week 2) → category + deadline/effort
features → **XGBoost predicts priority** → workload balancer suggests the
assignee (notebook 08).
