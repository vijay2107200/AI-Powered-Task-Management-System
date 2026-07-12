# Dataset Documentation — Week 1 (Dataset Collection)

**Project:** AI-Powered Task Management System
**Prepared by:** Vijayasiva
**Date:** 12 July 2026

---

## 1. Dataset Source

- **Name:** Synthetic Task Management Dataset
- **Type:** Synthetic dataset, generated in-repo (the project brief allows Trello/Jira API exports **or synthetic task datasets**; a synthetic source avoids API keys, rate limits and licensing issues while giving full control over labels)
- **Generator:** `scripts/generate_task_dataset.py` (seeded with `42` — fully reproducible)
- **File in repo:** `data/raw/tasks.csv` (8,110 rows)
- **Design references:** field structure modelled on Jira/Trello task exports (id, description, priority, due date, assignee, story points)

## 2. Problem Statement

The system must **automatically classify, prioritize and assign tasks** based on their descriptions, deadlines and user workloads. This dataset supports all three goals:

- **Week 2 — task classification:** predict `category` from the task description text (NLP: TF-IDF / embeddings → Naive Bayes, SVM)
- **Week 3 — priority prediction:** predict `priority` from text + numeric features (Random Forest / XGBoost)
- **Week 3 — workload balancing:** use `assignee_open_tasks`, `assignee_experience_years` and `estimated_hours` for assignment logic

## 3. Dataset Overview

| Property | Value |
|---|---|
| Rows (tasks) | 8,110 (includes ~110 injected duplicates for the cleaning stage) |
| Columns | 12 |
| Text feature | `task_description` (free text, avg ~10 words) |
| Classification target (Week 2) | `category` — 7 classes |
| Priority target (Week 3) | `priority` — 4 classes |
| Assignees | 25 simulated users |
| Time span | Jan–Jul 2026 |

## 4. Column Descriptions

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `task_id` | string | Unique task identifier (`TASK-10000` …) |
| 2 | `task_description` | text | Free-text description of the task — input for NLP preprocessing |
| 3 | `category` | category | Task type: Bug Fix, Feature, Testing, Maintenance, Documentation, Deployment, Research — **Week 2 target** |
| 4 | `priority` | category | Low / Medium / High / Critical — **Week 3 target** |
| 5 | `status` | category | Open, In Progress, Completed, Blocked |
| 6 | `created_date` | date | Date the task was created |
| 7 | `due_date` | date | Deadline for the task |
| 8 | `estimated_hours` | float | Estimated effort in hours (has missing values) |
| 9 | `story_points` | float | Agile story points: 1, 2, 3, 5, 8, 13 (has missing values) |
| 10 | `assignee_id` | string | Simulated user the task is assigned to (`USER-01` … `USER-25`) |
| 11 | `assignee_experience_years` | float | Experience of the assignee in years (has missing values) |
| 12 | `assignee_open_tasks` | int | Current number of open tasks of the assignee (workload signal) |

## 5. Target Variables

**`category` (Week 2 classification):** Bug Fix (~28%) and Feature (~25%) dominate; Research (~5%) is the smallest class.

**`priority` (Week 3 prediction):** Medium ~33%, Low ~30%, High ~19%, Critical ~17% — mildly imbalanced, as on real task boards. Priority was generated to correlate with deadline pressure, estimated effort and category, so it is genuinely learnable rather than random.

## 6. Known Data-Quality Issues (handled in the Week 1 cleaning notebook)

These issues were deliberately included so the cleaning stage reflects real-world data work:

1. **Missing values:** `estimated_hours` (~180), `assignee_experience_years` (~120), `story_points` (~60)
2. **Duplicate records:** ~110 exact duplicate rows
3. **Inconsistent category labels:** mixed casing (`bug fix`, `BUG FIX`) and stray trailing whitespace
4. **Whitespace noise** in some task descriptions; some descriptions carry urgency markers (`URGENT:`, `ASAP -`) that the NLP stage must normalise

## 7. Why This Dataset Is Suitable for the Project

1. **Matches the brief exactly** — task-level records with free-text descriptions, priorities, deadlines and workload fields, as required for classification, prioritization and assignment.
2. **Real text for NLP** — every task has a natural-language description, so tokenization, stop-word removal and lemmatization (Week 1) and TF-IDF/embeddings (Week 2) operate on genuine text.
3. **Learnable labels** — categories are reflected in the wording of descriptions and priority correlates with deadlines/effort, so Week 2–3 models have real signal to find.
4. **Realistically imperfect** — missing values, duplicates and inconsistent labels give the EDA/cleaning stage genuine work.
5. **Reproducible and unencumbered** — regenerate identical data any time with one script; no API credentials or licensing constraints.
