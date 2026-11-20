import pandas as pd

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/generated/training_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print()
print("Columns:")
print(df.columns.tolist())


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print()
print("=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

print(df["index_recommended"].value_counts().sort_index())

print()
print("Percentage:")

print(
    (df["index_recommended"].value_counts(normalize=True)
     .sort_index() * 100)
    .round(2)
)


# ============================================================
# TARGET BY QUERY TYPE
# ============================================================

print()
print("=" * 60)
print("TARGET BY QUERY TYPE")
print("=" * 60)

print(
    pd.crosstab(
        df["query_type"],
        df["index_recommended"]
    )
)


# ============================================================
# TARGET BY TABLE
# ============================================================

print()
print("=" * 60)
print("TARGET BY TABLE")
print("=" * 60)

print(
    pd.crosstab(
        df["table"],
        df["index_recommended"]
    )
)


# ============================================================
# TARGET BY COLUMN
# ============================================================

print()
print("=" * 60)
print("TARGET BY COLUMN")
print("=" * 60)

print(
    pd.crosstab(
        df["column"],
        df["index_recommended"]
    )
)


# ============================================================
# IMPROVEMENT BY TARGET
# ============================================================

print()
print("=" * 60)
print("IMPROVEMENT BY TARGET")
print("=" * 60)

print(
    df.groupby("index_recommended")["improvement_percent"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(3)
)


# ============================================================
# ABSOLUTE IMPROVEMENT BY TARGET
# ============================================================

print()
print("=" * 60)
print("ABSOLUTE IMPROVEMENT BY TARGET")
print("=" * 60)

print(
    df.groupby("index_recommended")["absolute_improvement_ms"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(3)
)


# ============================================================
# COST BEFORE BY TARGET
# ============================================================

print()
print("=" * 60)
print("COST BEFORE BY TARGET")
print("=" * 60)

print(
    df.groupby("index_recommended")["cost_before"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(3)
)


# ============================================================
# EXECUTION TIME BEFORE BY TARGET
# ============================================================

print()
print("=" * 60)
print("EXECUTION TIME BEFORE BY TARGET")
print("=" * 60)

print(
    df.groupby("index_recommended")["execution_time_before"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(3)
)


# ============================================================
# EXECUTION TIME AFTER BY TARGET
# ============================================================

print()
print("=" * 60)
print("EXECUTION TIME AFTER BY TARGET")
print("=" * 60)

print(
    df.groupby("index_recommended")["execution_time_after"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(3)
)


# ============================================================
# SCAN TYPE
# ============================================================

print()
print("=" * 60)
print("SCAN TYPE BY TARGET")
print("=" * 60)

print(
    pd.crosstab(
        df["scan_before"],
        df["index_recommended"]
    )
)


# ============================================================
# NEGATIVE LABELS WITH LARGE IMPROVEMENT
# ============================================================

print()
print("=" * 60)
print("NEGATIVE LABELS WITH LARGE IMPROVEMENT")
print("=" * 60)

negative_large = df[
    (df["index_recommended"] == 0) &
    (df["improvement_percent"] >= 20)
]

print(f"Count: {len(negative_large)}")

if len(negative_large) > 0:
    print(
        negative_large[
            [
                "table",
                "column",
                "query_type",
                "improvement_percent",
                "absolute_improvement_ms"
            ]
        ]
        .sort_values("improvement_percent", ascending=False)
        .head(20)
        .to_string(index=False)
    )


# ============================================================
# POSITIVE LABELS WITH SMALL ABSOLUTE IMPROVEMENT
# ============================================================

print()
print("=" * 60)
print("POSITIVE LABELS WITH SMALL ABSOLUTE IMPROVEMENT")
print("=" * 60)

positive_small = df[
    (df["index_recommended"] == 1) &
    (df["absolute_improvement_ms"] < 1)
]

print(f"Count: {len(positive_small)}")

if len(positive_small) > 0:
    print(
        positive_small[
            [
                "table",
                "column",
                "query_type",
                "improvement_percent",
                "absolute_improvement_ms"
            ]
        ]
        .sort_values("absolute_improvement_ms")
        .head(20)
        .to_string(index=False)
    )


# ============================================================
# DUPLICATE EXPERIMENTS
# ============================================================

print()
print("=" * 60)
print("DUPLICATE EXPERIMENTS")
print("=" * 60)

duplicate_columns = [
    "table",
    "column",
    "query_type",
    "test_value"
]

duplicates = df.duplicated(
    subset=duplicate_columns,
    keep=False
)

print(f"Duplicate rows: {duplicates.sum()}")

if duplicates.sum() > 0:
    print(
        df.loc[
            duplicates,
            duplicate_columns + ["index_recommended"]
        ]
        .sort_values(duplicate_columns)
        .head(30)
        .to_string(index=False)
    )


# ============================================================
# MISSING VALUES
# ============================================================

print()
print("=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = df.isnull().sum()

print(missing[missing > 0])

if missing.sum() == 0:
    print("No missing values.")


# ============================================================
# LABEL CONSISTENCY CHECK
# ============================================================

print()
print("=" * 60)
print("LABEL CONSISTENCY CHECK")
print("=" * 60)

expected_labels = (
    (df["improvement_percent"] >= 20.0) &
    (df["absolute_improvement_ms"] >= 1.0)
).astype(int)

mismatches = (expected_labels != df["index_recommended"]).sum()

print(f"Label mismatches: {mismatches}")


# ============================================================
# EXTREME IMPROVEMENTS
# ============================================================

print()
print("=" * 60)
print("EXTREME IMPROVEMENTS")
print("=" * 60)

print(
    df[
        [
            "table",
            "column",
            "query_type",
            "improvement_percent",
            "absolute_improvement_ms",
            "index_recommended"
        ]
    ]
    .sort_values("improvement_percent")
    .head(10)
    .to_string(index=False)
)

print()

print("Highest improvements:")

print(
    df[
        [
            "table",
            "column",
            "query_type",
            "improvement_percent",
            "absolute_improvement_ms",
            "index_recommended"
        ]
    ]
    .sort_values("improvement_percent", ascending=False)
    .head(10)
    .to_string(index=False)
)


# ============================================================
# DONE
# ============================================================

print()
print("=" * 60)
print("DATASET ANALYSIS COMPLETE")
print("=" * 60)