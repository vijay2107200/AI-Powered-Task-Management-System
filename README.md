# 🏥 Hospital Length-of-Stay Prediction — EDA & Insights

> Predicting how long a patient will stay in the hospital, before they even reach their bed.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4C72B0)](https://seaborn.pydata.org/)
[![Status](https://img.shields.io/badge/Status-EDA%20Complete-success)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)

---

## 📌 Overview

Hospitals lose millions in operational efficiency every year simply because they **don't know how long a patient will stay**. Bed allocation, staffing, and resource planning all hinge on this one number.

This project is a deep, ground-up **exploratory data analysis** of a real-world healthcare admissions dataset (**318,438 records**) with the goal of understanding what actually drives a patient's length of stay — before a single model gets trained.

> 🎯 **Goal:** Turn raw hospital admission data into a clean, model-ready dataset — backed by evidence, not guesswork.

---

## 🗂️ Table of Contents

- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Data Quality Summary](#-data-quality-summary)
- [Key EDA Findings](#-key-eda-findings)
- [Visual Highlights](#-visual-highlights)
- [Feature Engineering Roadmap](#-feature-engineering-roadmap)
- [Tech Stack](#-tech-stack)
- [How to Run](#-how-to-run)
- [Deliverables](#-deliverables)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 📊 Dataset

| | |
|---|---|
| **Rows** | 318,438 |
| **Columns** | 18 |
| **Target** | `Stay_Days` — 11 ordinal buckets (`0-10` → `More than 100 Days`) |
| **Domain** | Hospital admissions / healthcare analytics |
| **Grain** | One row per patient admission (`case_id`), with repeat patients (`patientid`) present |

<details>
<summary><b>📋 Full column reference (click to expand)</b></summary>

| Column | Type | Description |
|---|---|---|
| `case_id` | int | Unique admission record ID |
| `Hospital` | int (encoded) | Hospital identifier |
| `Hospital_type` | int (encoded) | Type/category of hospital |
| `Hospital_city` | int (encoded) | City code of hospital |
| `Hospital_region` | int (encoded) | Region code of hospital |
| `Available_Extra_Rooms_in_Hospital` | int | Extra rooms available at time of admission |
| `Department` | object | Medical department handling the case |
| `Ward_Type` | object | Ward category |
| `Ward_Facility` | object | Ward facility code |
| `Bed_Grade` | float (ordinal) | Quality grade of bed assigned |
| `patientid` | int | Patient identifier (repeats across visits) |
| `City_Code_Patient` | float (encoded) | Patient's home city code |
| `Type of Admission` | object | Emergency / Trauma / Urgent |
| `Illness_Severity` | object | Extreme / Moderate / Minor |
| `Patient_Visitors` | int | Number of visitors during stay |
| `Age` | object (ordinal) | Age bracket of patient |
| `Admission_Deposit` | float | Deposit amount paid at admission |
| `Stay_Days` | object (ordinal, **target**) | Length-of-stay bucket |

</details>

---

## 🏗️ Project Structure

```
hospital-los-prediction/
│
├── data/
│   ├── raw/
│   │   └── host_train.csv
│   └── processed/
│       └── train_clean.csv
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── reports/
│   └── figures/
│       ├── stay_days_distribution.png
│       ├── correlation_heatmap.png
│       └── categorical_vs_target/
│
├── README.md
└── requirements.txt
```

---

## ✅ Data Quality Summary

| Check | Result |
|---|---|
| Duplicate rows | ✅ None found |
| Missing values | ⚠️ Confined to `Bed_Grade` and `City_Code_Patient` (low volume, imputable) |
| Column naming issues | ⚠️ `Type of Admission` → renamed to `Admission_Type` |
| Repeat patients | ⚠️ Significant overlap in `patientid` — **must be handled during train/test split** to avoid leakage |
| Encoding | Several columns pre-encoded as integers (`Hospital`, `Hospital_city`, etc.) — not truly continuous |

> 🔑 **Verdict:** The dataset is large and clean enough to model directly after light imputation and a handful of structural fixes.

---

## 🔍 Key EDA Findings

1. **🎯 Imbalanced target.** `Stay_Days` is dominated by the `21-30` and `11-20` buckets, while long-stay buckets (`61-70`, `81-90`, `91-100`) are rare. → Stratified splitting + class weighting (or bucket consolidation) required.

2. **🩺 Illness_Severity and Type of Admission are real signal.** These features shift the *shape* of the stay-length distribution — not just the volume — making them strong predictive candidates.

3. **🏥 Department & Ward_Type are volume-skewed.** Gynecology and Wards R/S/Q dominate the dataset; rare categories should be grouped into `"Other"` to prevent sparse, noisy levels from destabilizing models.

4. **👤 Age has a moderate effect.** Signal is strongest and most reliable in the 31–60 bracket; very young/old groups are sparse.

5. **🔢 Ordinal features need ordinal encoding.** Both `Age` and `Stay_Days` are ordered string ranges — encoding them as arbitrary categories throws away valuable ordering information.

6. **📈 Skewed numeric features.** `Available_Extra_Rooms_in_Hospital` and `Patient_Visitors` are right-skewed with long tails → candidates for capping or log-transformation.

7. **💰 Admission_Deposit is clean.** Roughly bell-shaped, centered around ₹4,500–5,000 — ready for standard scaling with no major preprocessing needed.

---

## 🖼️ Visual Highlights

| Distribution of Stay Duration | Feature Relationships |
|:---:|:---:|
| Right-skewed, 11-bucket ordinal target with a long tail | Illness Severity & Admission Type reshape stay-length distribution |

*(Full visualizations — histograms, count plots, correlation heatmaps, and boxplots — are available in `notebooks/01_eda.ipynb`.)*

---

## 🛠️ Feature Engineering Roadmap

- [ ] Rename `Type of Admission` → `Admission_Type`
- [ ] Ordinal-encode `Age` and `Stay_Days`
- [ ] Group rare `Department` and `Ward_Type` categories into `"Other"`
- [ ] Impute `Bed_Grade` and `City_Code_Patient`
- [ ] Log-transform / cap outliers in `Patient_Visitors` and `Available_Extra_Rooms_in_Hospital`
- [ ] Patient-aware train/test split (group by `patientid`) to prevent leakage
- [ ] Evaluate bucket consolidation for extreme target class imbalance

---

## 🧰 Tech Stack

| Purpose | Tool |
|---|---|
| Data manipulation | `pandas`, `numpy` |
| Visualization | `matplotlib`, `seaborn` |
| Environment | Jupyter Notebook |
| Language | Python 3.9+ |

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/<your-username>/hospital-los-prediction.git
cd hospital-los-prediction

# Install dependencies
pip install -r requirements.txt

# Launch the EDA notebook
jupyter notebook notebooks/01_eda.ipynb
```

---

## 📦 Deliverables

- ✅ Cleaned dataset — `data/processed/train_clean.csv` (318,438 rows × 18 columns, missing values imputed)
- ✅ Full EDA notebook with all visualizations and written observations
- ✅ This README, documenting findings for reviewers, collaborators, and future-you

---

## 🗺️ Roadmap

- [x] **Week 1:** Data cleaning & exploratory data analysis
- [ ] **Week 2:** Feature engineering & ordinal encoding
- [ ] **Week 3:** Baseline modelling (Logistic Regression, Random Forest, XGBoost)
- [ ] **Week 4:** Class imbalance handling & hyperparameter tuning
- [ ] **Week 5:** Final model evaluation & deployment-ready pipeline

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**⭐ If this project helped you understand hospital length-of-stay data, consider starring the repo!**

</div>
