# Week 3 Plan — Priority Prediction & Workload Balancing

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Period:** 20 – 26 July 2026

## Goals (from the project brief)

1. Priority prediction model using Random Forest / XGBoost
2. Workload balancing logic using a heuristic or ML approach
3. GridSearchCV for hyperparameter tuning

## Task Allocation

### Member 1 — Coordination, Integration & Documentation
- Create and manage the Week 3 branches, review and merge PRs
- Keep `main` presentation-ready; maintain README, progress and meeting notes
- End-of-week integration check: a task goes in → priority comes out → assignee
  is suggested, all on the same data
- Prepare the Week 3 progress summary (`reports/week3_progress.md`)

### Member 2 — Priority Prediction: Random Forest
- Build the **priority feature matrix**: shared TF-IDF features from `models/` +
  `days_to_deadline`, `estimated_hours`, `story_points`, encoded `category`
- Save the matrix to `models/` so XGBoost uses identical features
- Train Random Forest on the **shared stratified split** (`train_idx`/`test_idx`)
- GridSearchCV over `n_estimators`, `max_depth`, `min_samples_leaf`, `class_weight`
- Report accuracy, macro precision/recall/F1, confusion matrix and a
  **feature-importance chart**
- Deliverable: `notebooks/06_Priority_RandomForest.ipynb`

### Member 3 — Priority Prediction: XGBoost
- Train XGBoost on the **same feature matrix and split** as Member 2
- GridSearchCV over `n_estimators`, `max_depth`, `learning_rate`, `subsample`
- Produce the combined **RF vs. XGBoost comparison** on the shared test split and
  recommend the final priority model for Week 4
- Deliverables: `notebooks/07_Priority_XGBoost.ipynb`,
  `reports/week3_priority_comparison.md`

### Member 4 — Workload Balancing Logic
- Heuristic assignment scoring using `assignee_open_tasks`,
  `assignee_experience_years` and estimated effort (heuristic chosen over ML —
  we have no historical assignment outcomes to learn from; document this)
- Simulate several hundred tasks through the balancer; visualize workload
  distribution across the 25 users **with vs. without** balancing
- Deliverables: `notebooks/08_Workload_Balancing.ipynb`,
  `scripts/workload_balancer.py` (reusable scoring function)

## Branch Workflow

| Branch | Owner | Purpose |
|---|---|---|
| `main` | Member 1 | Stable, review-ready — changes land via PR only |
| `week3-priority-rf` | Member 2 | Feature matrix + Random Forest notebook |
| `week3-priority-xgb` | Member 3 | XGBoost notebook + comparison report |
| `week3-workload` | Member 4 | Balancer module + simulation notebook |

Rules (unchanged from Week 2):
1. Work only on your own branch; PR to `main` when a deliverable is ready.
2. `week3-priority-rf` merges **first** — XGBoost depends on its saved feature matrix.
3. PRs need one review before merge; notebooks must be committed executed.
4. **Re-clone before starting** — history was cleaned after Week 2; do not pull
   into an old clone.

## Timeline

| Day | Milestone |
|---|---|
| Mon–Tue | Feature matrix saved and merged; balancer heuristic drafted |
| Wed–Thu | Both priority models tuned and evaluated; balancer simulation done |
| Fri | RF vs. XGB comparison merged; end-to-end integration check; progress summary |

## Week 3 Checklist

- [x] Priority feature matrix saved to `models/` (shared by both models)
- [x] Random Forest tuned (GridSearchCV) and evaluated on the shared split
- [x] XGBoost tuned (GridSearchCV) and evaluated on the shared split
- [x] RF vs. XGBoost comparison documented with a Week 4 recommendation
- [x] Workload balancer implemented, simulated and visualized
- [x] End-to-end integration verified (task → priority → suggested assignee) —
      see `notebooks/09_Integration_Check.ipynb`
