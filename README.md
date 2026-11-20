Explainable AI-Based Index Recommendation System for PostgreSQL Query Optimization

An explainable AI-powered system that analyzes SQL queries, recommends potentially useful indexes for PostgreSQL, and validates performance improvements through query execution plans and benchmarking.

Overview

PostgreSQL has a built-in cost-based query optimizer, but choosing appropriate indexes can still require database expertise and experimentation.

This project introduces an AI-assisted index recommendation system that combines machine learning, SQL analysis, explainable AI, and empirical database benchmarking to help users identify potentially beneficial indexes.

The system analyzes supported SQL queries, extracts relevant database statistics, predicts whether an index would be useful, explains the prediction using SHAP, and verifies the candidate index using PostgreSQL.

Key Features

SQL Query Analysis: Parses and analyzes supported PostgreSQL SELECT queries using SQLGlot.

Database Statistics Extraction: Retrieves table and column statistics from PostgreSQL.

ML-Based Index Recommendation: Uses a Random Forest classifier to predict whether a candidate index is beneficial.

Explainable AI: Uses SHAP to explain the factors influencing model predictions.

Performance Verification: Compares query execution plans and execution times before and after creating a candidate index.

Interactive Dashboard: Provides a Streamlit interface to enter SQL queries and inspect recommendations.

SQL Generation: Generates a CREATE INDEX statement for the recommended index.

System Architecture

The project consists of two main workflows.

1. Model Training Pipeline

Load the selected Olist e-commerce datasets into PostgreSQL.

Generate SQL query experiments.

Benchmark queries before and after creating candidate indexes.

Calculate performance improvements and generate binary labels.

Extract and engineer model features.

Train and evaluate a Random Forest classifier.

Save the trained model for application use.

2. Query Recommendation Pipeline

User enters a SQL query through the Streamlit dashboard.

SQLGlot parses the query and identifies supported predicates.

PostgreSQL statistics and execution plans are used to extract features.

The trained Random Forest model predicts index usefulness.

SHAP provides an explanation of the prediction.

PostgreSQL empirically tests the candidate index.

The dashboard displays execution-plan changes, benchmark results, and the suggested CREATE INDEX statement.

Workflow principle: The model predicts, SHAP explains, and PostgreSQL tests.

Technology Stack

Component

Technology

Programming Language

Python

Database

PostgreSQL

SQL Parsing

SQLGlot

Machine Learning

Scikit-learn

Model

Random Forest Classifier

Explainable AI

SHAP

Data Processing

Pandas, NumPy

Dashboard

Streamlit

Database Connectivity

Psycopg2

Model Persistence

Joblib

Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist, obtained from Kaggle.

The original dataset contains nine relational tables. This project uses five selected tables:

Orders

Customers

Order Items

Products

Sellers

The original raw datasets are excluded from this repository because of their size. The generated training and ML datasets are included.

Index usefulness labels are generated through the project's own PostgreSQL benchmarking experiments rather than being provided by the original Olist dataset.

Dataset Preparation

Download the Olist dataset from Kaggle and place the required CSV files in:

data/raw/olist/

The selected files are:

olist_orders_dataset.csv

olist_customers_dataset.csv

olist_order_items_dataset.csv

olist_products_dataset.csv

olist_sellers_dataset.csv

Model Training and Evaluation

The final machine learning dataset contains:

513 experiment records

27 predictor features

1 target variable

378 positive samples

135 negative samples

The target variable, index_recommended, indicates whether the candidate index satisfies both project-specific performance thresholds:

At least 20% relative execution-time improvement.

At least 1 ms absolute execution-time improvement.

Model Evaluation

The Random Forest classifier was evaluated using 5-fold Stratified Group Cross-Validation.

Metric

Score

Accuracy

95.15%

Precision

97.31%

Recall

96.13%

F1-Score

96.64%

ROC-AUC

96.21%

Group-based validation helps reduce leakage between related table-column-query groups.

These results reflect the constructed Olist benchmark dataset and should not be interpreted as guaranteed performance on unseen database schemas.

Explainability with SHAP

SHAP (SHapley Additive exPlanations) is used to understand how individual features influence the model's predictions.

The important features include:

Selectivity

Value Frequency

Query Cost Before Indexing

Column and Table Characteristics

SHAP explanations help users understand why the classifier predicts that a candidate index may be useful.

SHAP explains model behaviour; it does not establish causality.

Performance Benchmarking

The system verifies recommendations using actual PostgreSQL query execution.

A recorded experiment using an equality query on orders.customer_id produced the following results:

Metric

Before Index

After Index

Execution Time

10.027 ms

0.039 ms

Estimated Query Cost

3581.01

8.44

Scan Type

Sequential Scan

Index Scan

Recorded execution-time improvement: approximately 99.61%.

Execution times may vary depending on database configuration, caching, hardware, and system load.

The candidate index is created for verification and dropped afterwards. The application provides the suggested SQL statement for the user to review; it does not automatically create a permanent index.

Supported SQL Queries

The current implementation focuses on single-table SELECT queries containing a WHERE clause.

Supported predicate types include:

Equality (=)

IN

Range comparisons (<, >, <=, >=)

BETWEEN

IS NOT NULL

The current advisor does not provide full index recommendations for JOIN predicates, GROUP BY, HAVING, correlated subqueries, or general ORDER BY-only workloads.

Project Structure

postgresql-ai-index-advisor/
│
├── data/
│   └── generated/
│       ├── ml_dataset.csv
│       ├── ml_dataset_v1.csv
│       ├── training_data.csv
│       └── training_data_v1.csv
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
└── requirements.txt

Installation and Setup

1. Clone the Repository

git clone https://github.com/Tiyashaghosh/postgresql-ai-index-advisor.git
cd postgresql-ai-index-advisor

2. Create a Virtual Environment

Using Conda:

conda create -n query_optimizer python=3.12
conda activate query_optimizer

3. Install Dependencies

pip install -r requirements.txt

4. Configure PostgreSQL

Create a PostgreSQL database named:

CREATE DATABASE query_optimizer;

Load the required Olist tables into PostgreSQL before running the application.

5. Configure Environment Variables

Create a .env file in the project root:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=query_optimizer
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

Replace the password with your local PostgreSQL password.

Important: Never commit your .env file or expose database credentials publicly.

6. Run the Application

streamlit run src/app.py

The Streamlit dashboard should open in your browser.

Limitations

The training dataset is based on five selected Olist tables.

The number of table-column-query groups is limited.

The model's generalization to unseen database schemas requires further evaluation.

Benchmark execution times can vary due to caching and system conditions.

Current recommendations focus on individual queries rather than workload-wide optimization.

Index storage costs and write-operation overhead are not included in the current recommendation objective.

SQL support is limited to the implemented query patterns.

Future Enhancements

Expand evaluation across additional databases and schemas.

Support JOIN-based and more complex SQL queries.

Explore composite index recommendations.

Incorporate workload-level optimization.

Account for index storage and write-maintenance overhead.

Compare additional machine learning models.

Improve benchmark reproducibility and index-cleanup safety.



SRM Institute of Science and Technology

An academic project exploring the integration of machine learning, explainable AI, and PostgreSQL query optimization.
