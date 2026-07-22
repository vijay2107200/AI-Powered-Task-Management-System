# Summary Dashboard — Usage Note

`app/dashboard.py` is the Week 4 "summary dashboard/mockup" deliverable: a
Streamlit interface where you paste a task description + deadline/effort and
get back a predicted category, predicted priority, and suggested assignee,
plus a live team workload chart.

## What's real vs. placeholder

| Piece | Status | Source |
|---|---|---|
| Assignee suggestion | ✅ **Real** | `scripts/workload_balancer.py` (Week 3 deliverable, validated in `notebooks/08_Workload_Balancing.ipynb`) |
| Category prediction | ⚠️ Placeholder heuristic | keyword matching in `dashboard.py` |
| Priority prediction | ⚠️ Placeholder heuristic | deadline/effort rule in `dashboard.py` |

Category and priority are still placeholders because notebooks 03–07
(feature extraction, Naive Bayes/SVM classifiers, priority model) haven't
landed yet — there's no trained model artifact to load for those two. The
assignee step, however, now uses the actual `WorkloadBalancer` scoring
engine: experience-fit vs. task difficulty, minus a live workload penalty,
exactly as validated in the notebook (93% reduction in workload std-dev
vs. the as-recorded baseline).

The dashboard keeps one live `WorkloadBalancer` per session — each
"Predict + Assign" click both suggests *and* commits an assignment (like
the notebook's `assign()`), so the workload chart updates in real time as
you add tasks. Use **Reset workload** to return to the starting snapshot.

Once the classifier/priority notebooks land, swap in the real model calls
inside `predict_category()` and `predict_priority()` in `dashboard.py` — no
other part of the app (layout, chart, assignment logic) needs to change.

## Run it

```bash
pip install streamlit pandas
streamlit run app/dashboard.py   # run from the repo root
```

Opens at `http://localhost:8501`. Enter a task description, pick a
deadline, set estimated effort, and click **Predict + Assign**.

## File layout

```
scripts/
└── workload_balancer.py   # real assignee-scoring engine (Week 3)
app/
├── dashboard.py            # the Streamlit dashboard
└── README.md                # this file
```
