import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# PATHS
# ============================================================

ML_DATA_PATH = "data/generated/ml_dataset.csv"
RAW_DATA_PATH = "data/generated/training_data.csv"
MODEL_PATH = "models/index_recommender.pkl"

TARGET = "index_recommended"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("LOADING DATA")
print("=" * 60)

ml_df = pd.read_csv(ML_DATA_PATH)
raw_df = pd.read_csv(RAW_DATA_PATH)

X = ml_df.drop(columns=[TARGET])
y = ml_df[TARGET]


print(f"Rows   : {len(ml_df)}")
print(f"Columns: {len(ml_df.columns)}")


# ============================================================
# CREATE GROUPS
# ============================================================

groups = (
    raw_df["table"].astype(str)
    + "_"
    + raw_df["column"].astype(str)
    + "_"
    + raw_df["query_type"].astype(str)
)


print()
print("=" * 60)
print("GROUP INFORMATION")
print("=" * 60)

print(f"Unique groups: {groups.nunique()}")

print()
print("Largest groups:")

print(
    groups.value_counts()
    .head(10)
)


# ============================================================
# STRATIFIED GROUP K-FOLD
# ============================================================

print()
print("=" * 60)
print("5-FOLD STRATIFIED GROUP CROSS-VALIDATION")
print("=" * 60)

cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


accuracies = []
roc_aucs = []
precisions = []
recalls = []
f1_scores = []


for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups),
    start=1
):

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    train_groups = set(groups.iloc[train_idx])
    test_groups = set(groups.iloc[test_idx])

    overlap = train_groups.intersection(test_groups)

    print()
    print(f"FOLD {fold}")
    print("-" * 40)

    print(f"Training samples: {len(train_idx)}")
    print(f"Testing samples : {len(test_idx)}")

    print(f"Training groups : {len(train_groups)}")
    print(f"Testing groups  : {len(test_groups)}")

    print(f"Group overlap   : {len(overlap)}")

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    accuracies.append(accuracy)
    roc_aucs.append(roc_auc)
    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")


# ============================================================
# CROSS-VALIDATION SUMMARY
# ============================================================

print()
print("=" * 60)
print("CROSS-VALIDATION RESULTS")
print("=" * 60)

print(
    f"Accuracy : {np.mean(accuracies):.4f} "
    f"+/- {np.std(accuracies):.4f}"
)

print(
    f"ROC-AUC  : {np.mean(roc_aucs):.4f} "
    f"+/- {np.std(roc_aucs):.4f}"
)

print(
    f"Precision: {np.mean(precisions):.4f} "
    f"+/- {np.std(precisions):.4f}"
)

print(
    f"Recall   : {np.mean(recalls):.4f} "
    f"+/- {np.std(recalls):.4f}"
)

print(
    f"F1-score : {np.mean(f1_scores):.4f} "
    f"+/- {np.std(f1_scores):.4f}"
)


# ============================================================
# TRAIN FINAL MODEL ON ALL DATA
# ============================================================

print()
print("=" * 60)
print("TRAINING FINAL MODEL")
print("=" * 60)

final_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

final_model.fit(X, y)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": final_model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print()
print("TOP 15 FEATURES")
print("-" * 60)

print(
    importance.head(15).to_string(index=False)
)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)

joblib.dump(
    final_model,
    MODEL_PATH
)

print()
print("=" * 60)
print("FINAL MODEL SAVED")
print("=" * 60)

print(f"Location: {MODEL_PATH}")

print()
print("=" * 60)
print("PHASE 1 COMPLETE")
print("=" * 60)