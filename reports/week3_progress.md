# Week 3 Progress Summary — Priority Prediction & Workload Balancing

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Period:** 20 – 26 July 2026

## 1. Deliverable Status

| Deliverable (from `docs/WEEK3_PLAN.md`) | Owner | Status | Location |
|---|---|---|---|
| Priority feature matrix (shared) | Member 2/3 | ✅ Done | `models/priority_X_train.joblib`, `priority_X_test.joblib` |
| Random Forest priority model (GridSearchCV) | Member 2 | ✅ Done | `notebooks/06_Priority_RandomForest.ipynb` |
| XGBoost priority model (GridSearchCV) | Member 3 | ✅ Done | `notebooks/07_Priority_XGBoost.ipynb` |
| RF vs. XGBoost comparison + Week 4 recommendation | Member 3 | ✅ Done | `reports/week3_priority_comparison.md` |
| Workload balancer + simulation | Member 4 | ✅ Done | `notebooks/08_Workload_Balancing.ipynb`, `scripts/workload_balancer.py` |
| End-to-end integration check | Member 1 | ✅ Done | `notebooks/09_Integration_Check.ipynb` |

## 2. Model Results (shared stratified test split)

| Model | Features | Accuracy | Macro Precision | Macro Recall | Macro F1 |
|---|---|---|---|---|---|
| Random Forest | TF-IDF + numeric | 0.559 | 0.557 | 0.556 | 0.538 |
| **XGBoost (tuned)** | TF-IDF + numeric | **0.631** | **0.644** | **0.636** | **0.638** |

**Recommendation:** XGBoost carries forward to Week 4 — it beats Random Forest on
every metric, and both models agree `days_to_deadline` is the dominant signal
(confirming the Week 1 EDA). Full analysis in `reports/week3_priority_comparison.md`.

Reference baseline from Week 2 (category classification, same split discipline):
Linear SVM on TF-IDF — accuracy 0.815, macro F1 0.795. Priority scores sit lower
because priority is intrinsically noisier — generated from continuous
deadline/effort signals plus 5% label noise, so class boundaries genuinely overlap.

### Workload balancer

Simulated by replaying 300 tasks chronologically through both the as-recorded
baseline assignment and the heuristic balancer, starting from identical initial
workload state:

| Scenario | Std. dev across 25 users | Range (max − min) |
|---|---|---|
| Starting state | 5.8 | 18 |
| Baseline (as-recorded) | 7.5 | 24 |
| **With balancer** | **0.56** | **2** |

The balancer reduces workload imbalance by ~93% relative to the as-recorded
baseline — see `notebooks/08_Workload_Balancing.ipynb` section 4–5.

## 3. Integration Check (end of week) — ✅ Verified

Pipeline verified in `notebooks/09_Integration_Check.ipynb`, using only the
committed Week 2–3 artifacts (no retraining):

1. Raw task description → Week 1 preprocessing → shared TF-IDF vectorizer
2. → **SVM** predicts category (Week 2)
3. → category + deadline/effort features → **XGBoost** predicts priority (Week 3)
4. → **WorkloadBalancer** suggests an assignee (Week 3)

Run on 5 unseen example task descriptions:

| Description (truncated) | Category | Priority | Assignee |
|---|---|---|---|
| "URGENT: payment gateway crashes on checkout…" | Bug Fix | Critical | USER-23 |
| "Write the onboarding documentation for…" | Documentation | Low | USER-16 |
| "Add dark mode support to the admin panel…" | Feature | Low | USER-16 |
| "Investigate why the notification service…" | Bug Fix | High | USER-12 |
| "Set up automated regression tests for…" | Testing | Medium | USER-05 |

- [x] Steps run end-to-end from the committed artifacts in `models/` and `scripts/`
- [x] Suggested assignees respect workload and experience constraints (5 checks
      passed, including that a 1-day-deadline urgent task correctly ranks
      Medium+ and that the balancer spreads work across multiple people)
- [x] Example walkthrough recorded above for the Week 4 dashboard/demo

## 4. Risks / Notes

- `priority` is milder in imbalance than `category` (Critical ~17%), but macro
  metrics and stratified splits remain the standard
- XGBoost requires `pip install xgboost` (Python ≤3.13 venv, same as gensim)
- Notebook 06 (Random Forest) and the workload notebook originally shipped with
  foreign-machine absolute paths and a wrong file extension; both were fixed
  and re-executed on the current repo artifacts
- Re-clone before Week 4 work — history was cleaned up after Week 2 and again
  after Week 3 branch cleanup; do not pull into an old clone
