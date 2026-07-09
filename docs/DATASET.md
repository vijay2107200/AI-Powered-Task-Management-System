# Dataset Documentation — Week 1 (Dataset Collection)

**Prepared by:** Vijayasiva
**Date:** 09 July 2026

---

## 1. Dataset Source

- **Name:** AV: Healthcare Analytics II
- **Source:** Kaggle — https://www.kaggle.com/datasets/nehaprabhavalkar/av-healthcare-analytics-ii
- **Original origin:** Analytics Vidhya "JanataHack: Healthcare Analytics II" hackathon
- **License / usage:** Public dataset shared on Kaggle for educational and research purposes
- **File in repo:** `data/raw/train.csv` (~27 MB)

## 2. Problem Statement

The dataset is designed for predicting the **Length of Stay (LOS)** of a patient admitted to a hospital. Length of Stay is a critical metric for hospital management: accurate prediction helps hospitals optimize bed allocation, plan resources, reduce waiting time, and lower the risk of infection from overstaying patients.

This is a **multi-class classification** problem with 11 possible classes.

## 3. Dataset Overview

| Property | Value |
|---|---|
| Rows (hospital admission cases) | 318,438 |
| Columns | 18 (17 features + 1 target) |
| Unique patients | 92,017 (patients can have multiple admissions) |
| Duplicate rows | 0 |
| Missing values | `Bed_Grade`: 113, `City_Code_Patient`: 4,532 |

## 4. Column Descriptions

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `case_id` | int | Unique ID for each admission case (identifier — not a predictive feature) |
| 2 | `Hospital` | int | Unique code of the hospital (32 hospitals) |
| 3 | `Hospital_type` | int | Code for the type of hospital (7 types) |
| 4 | `Hospital_city` | int | City code where the hospital is located (11 cities) |
| 5 | `Hospital_region` | int | Region code of the hospital (3 regions) |
| 6 | `Available_Extra_Rooms_in_Hospital` | int | Number of extra rooms available in the hospital at admission (0–24) |
| 7 | `Department` | category | Overlooking department: gynecology, anesthesia, radiotherapy, surgery, TB & Chest disease |
| 8 | `Ward_Type` | category | Code of the ward (P, Q, R, S, T, U) |
| 9 | `Ward_Facility` | category | Code of the ward facility (A–F) |
| 10 | `Bed_Grade` | float | Condition/grade of the bed in the ward (1.0–4.0); **113 missing values** |
| 11 | `patientid` | int | Unique patient ID (a patient can appear in multiple cases) |
| 12 | `City_Code_Patient` | float | City code of the patient (37 cities); **4,532 missing values** |
| 13 | `Type of Admission` | category | Emergency, Trauma, or Urgent |
| 14 | `Illness_Severity` | category | Severity of the illness at admission: Minor, Moderate, Extreme |
| 15 | `Patient_Visitors` | int | Number of visitors with the patient (0–32) |
| 16 | `Age` | category | Age of the patient, binned in 10-year ranges (0-10 … 91-100) |
| 17 | `Admission_Deposit` | float | Deposit paid at admission (1,800 – 11,008; mean ≈ 4,881) |
| 18 | **`Stay_Days`** | category | **TARGET** — length of stay, binned into 11 classes |

## 5. Target Variable — `Stay_Days`

11 classes representing the length of stay in days:

| Class | Count | Share |
|---|---|---|
| 0-10 | 23,604 | 7.4% |
| 11-20 | 78,139 | 24.5% |
| 21-30 | 87,491 | 27.5% |
| 31-40 | 55,159 | 17.3% |
| 41-50 | 11,743 | 3.7% |
| 51-60 | 35,018 | 11.0% |
| 61-70 | 2,744 | 0.9% |
| 71-80 | 10,254 | 3.2% |
| 81-90 | 4,838 | 1.5% |
| 91-100 | 2,765 | 0.9% |
| More than 100 Days | 6,683 | 2.1% |

**Note:** The classes are **imbalanced** — the majority of stays fall in the 11–40 day range (~69%), while several long-stay classes are under 2%. This must be handled during modelling (e.g., class weights, stratified splits, or resampling).

## 6. Why This Dataset Is Suitable for Our Project

1. **Large and realistic** — 318k real-world admission records give enough data to train and properly validate ML models without overfitting concerns.
2. **Rich mix of feature types** — numeric, ordinal, and categorical features allow the team to practice the full preprocessing pipeline (encoding, scaling, handling missing values) planned for Weeks 2–3.
3. **Clean but not too clean** — it has a small, manageable amount of missing data (`Bed_Grade`, `City_Code_Patient`) and class imbalance, which gives Sanjay real EDA/cleaning work and makes the project realistic.
4. **Well-defined supervised target** — `Stay_Days` is a clear multi-class classification target with a meaningful business interpretation (resource planning and bed management for hospitals).
5. **Well-known benchmark** — it comes from a public Analytics Vidhya hackathon, so published leaderboard scores exist that we can compare our model's accuracy against.

## 7. Notes / Observations for the Team

- The file was originally downloaded as `host_train.csv.xls` — despite the extension it is a **plain CSV** and has been renamed to `data/raw/train.csv`.
- `case_id` and `patientid` are identifiers, not features. However, `patientid` repeats (92k patients across 318k cases), so patient-level aggregate features (e.g., number of previous admissions) could be engineered later.
- `Age` and `Stay_Days` are stored as string ranges (e.g., "21-30") and will need ordinal encoding.
- The column `Type of Admission` contains spaces in its name — handle carefully in code (rename recommended during cleaning).
