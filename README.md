
# PostgreSQL AI Index Advisor

### Explainable AI-Based Index Recommendation System for Query Optimization

An AI-powered PostgreSQL index advisor that analyzes SQL queries, predicts potentially useful indexes, explains its recommendations using SHAP, and validates performance improvements through database benchmarking.

<p align="center">
  <b>Python · PostgreSQL · Scikit-learn · SHAP · Streamlit</b>
</p>

---

## Overview

PostgreSQL has a built-in cost-based query optimizer. However, identifying appropriate indexes and understanding their performance impact can still require manual experimentation.

This project introduces an **AI-assisted index recommendation system** that combines machine learning, SQL analysis, explainable AI, and empirical benchmarking.

The system:

1. Analyzes supported SQL queries.
2. Extracts relevant PostgreSQL statistics.
3. Predicts whether a candidate index is beneficial.
4. Explains the prediction using SHAP.
5. Tests the candidate index against PostgreSQL.
6. Presents the recommendation and generated SQL statement through an interactive dashboard.

> **The model predicts. SHAP explains. PostgreSQL tests.**

---

## Key Features

| Feature | Description |
|---|---|
| SQL Analysis | Parses supported PostgreSQL SELECT queries using SQLGlot |
| Feature Extraction | Retrieves table and column statistics from PostgreSQL |
| ML Prediction | Uses a Random Forest classifier to predict index usefulness |
| Explainable AI | Uses SHAP to interpret model predictions |
| Performance Testing | Compares execution plans and execution times before and after indexing |
| Interactive Dashboard | Provides a Streamlit interface for query analysis |
| SQL Generation | Generates CREATE INDEX statements for user review |

---

## System Architecture

### 1. Model Training Pipeline

```text
Olist Dataset
      |
      v
PostgreSQL Database
      |
      v
SQL Experiment Generation
      |
      v
Before/After Index Benchmarking
      |
      v
Performance-Based Label Generation
      |
      v
Feature Engineering
      |
      v
Random Forest Training
      |
      v
Model Evaluation & Saving
```

### 2. Query Recommendation Pipeline

```text
       User SQL Query
              |
              v
       SQLGlot Parsing
              |
              v
   PostgreSQL Statistics
              |
              v
      Feature Extraction
              |
              v
    Random Forest Model
              |
              v
       Index Prediction
              |
       +------+------+
       |             |
       v             v
  SHAP Explanation   PostgreSQL
                     Verification
       |             |
       +------+------+
              |
              v
     Recommendation Dashboard
              |
              v
      CREATE INDEX Statement
```

---

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Database | PostgreSQL |
| SQL Parsing | SQLGlot |
| Machine Learning | Scikit-learn |
| ML Algorithm | Random Forest |
| Explainability | SHAP |
| Data Processing | Pandas, NumPy |
| Dashboard | Streamlit |
| Database Connectivity | Psycopg2 |
| Model Persistence | Joblib |

---

## Dataset

**Brazilian E-Commerce Public Dataset by Olist — Kaggle**

The original dataset contains nine relational tables. This project uses five selected tables:

- Orders
- Customers
- Order Items
- Products
- Sellers

The original Olist dataset does not contain index-usefulness labels. These labels are generated through custom PostgreSQL benchmarking experiments.

### Training Dataset

| Property | Value |
|---|---:|
| Experiment records | 513 |
| Predictor features | 27 |
| Target variables | 1 |
| Positive samples | 378 |
| Negative samples | 135 |

The target variable `index_recommended` is generated using two project-specific performance thresholds:

- Relative execution-time improvement ≥ 20%
- Absolute execution-time improvement ≥ 1 ms

---

## Machine Learning Results

**Model:** Random Forest Classifier

**Validation:** 5-Fold Stratified Group Cross-Validation

| Evaluation Metric | Score |
|---|---:|
| Accuracy | **95.15%** |
| Precision | **97.31%** |
| Recall | **96.13%** |
| F1-Score | **96.64%** |
| ROC-AUC | **96.21%** |

Group-based validation helps reduce leakage between related table-column-query groups.

*These results represent evaluation on the constructed Olist benchmark dataset and do not guarantee equivalent performance on unseen database schemas.*

---

## Explainable AI with SHAP

SHAP (SHapley Additive exPlanations) is used to explain how individual features influence the Random Forest model's predictions.

Important features include:

1. Selectivity
2. Value Frequency
3. Query Cost Before Indexing
4. Column and Table Characteristics

SHAP helps users understand which features push a prediction towards or away from recommending an index.

---

## Performance Benchmark

A recorded experiment using an equality query on `orders.customer_id` produced the following results:

| Metric | Before Index | After Index |
|---|---:|---:|
| Execution Time | 10.027 ms | 0.039 ms |
| Estimated Query Cost | 3581.01 | 8.44 |
| Scan Type | Sequential Scan | Index Scan |

<details>
<summary><strong>View benchmark improvement</strong></summary>

- Absolute execution-time reduction: **9.988 ms**
- Relative execution-time improvement: **99.61%**
- Query plan changed from Sequential Scan to Index Scan.

Execution times can vary depending on hardware, caching, database configuration and system load.

</details>

The candidate index is created for verification and dropped afterwards. The application generates the suggested SQL statement for the user to review; it does not automatically create a permanent index.

---

## Supported SQL Queries

The current implementation focuses on single-table SELECT queries containing a WHERE clause.

| Predicate Type | Supported |
|---|---|
| Equality (`=`) | Yes |
| IN | Yes |
| Range comparisons | Yes |
| BETWEEN | Yes |
| IS NOT NULL | Yes |
| JOIN-based index recommendations | No |
| GROUP BY / HAVING | No |
| Correlated subqueries | No |
| General ORDER BY-only workloads | No |

---

## Project Structure

```text
postgresql-ai-index-advisor/
│
├── data/
│   └── generated/
│
├── models/
│   └── index_recommender.pkl
│
├── scripts/
│   ├── analyze_dataset.py
│   ├── benchmark_indexes.py
│   ├── build_ml_dataset.py
│   ├── generate_training_data.py
│   ├── load_olist.py
│   └── train_model.py
│
├── src/
│   ├── app.py
│   ├── explain_prediction.py
│   └── sql_recommender.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### Prerequisites

- Python 3.12
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Tiyashaghosh/postgresql-ai-index-advisor.git

cd postgresql-ai-index-advisor
```

### 2. Create a Virtual Environment

Using Conda:

```bash
conda create -n query_optimizer python=3.12

conda activate query_optimizer
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a database:

```sql
CREATE DATABASE query_optimizer;
```

Download the required Olist CSV files from Kaggle and place them inside:

```text
data/raw/olist/
```

Load the required tables into PostgreSQL using the provided project scripts.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=query_optimizer
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

**Never upload your `.env` file or expose database credentials on GitHub.**

### 6. Run the Application

```bash
streamlit run src/app.py
```

The Streamlit dashboard should open in your browser.

---

## Limitations

- Training data is based on five selected Olist tables.
- Only 20 table-column-query groups are represented.
- Generalization to unseen database schemas requires further evaluation.
- Benchmark execution times are affected by caching and system conditions.
- Current recommendations focus on individual queries rather than workload-wide optimization.
- Index storage and write-maintenance overhead are not included in the current recommendation objective.
- SQL support is limited to the implemented query patterns.

## Future Enhancements

- Extend evaluation to additional databases and schemas.
- Support JOIN-based and more complex SQL queries.
- Explore composite index recommendations.
- Introduce workload-level index optimization.
- Account for index storage and write-maintenance costs.
- Compare additional machine learning algorithms.
- Improve benchmark reproducibility and safe index cleanup.

---

## Author

**Tiyasha Ghosh**

B.Tech – Computer Science and Engineering (AI & ML)

SRM Institute of Science and Technology

---

<p align="center">
  <i>An academic project integrating Machine Learning, Explainable AI and PostgreSQL Query Optimization.</i>
</p>
