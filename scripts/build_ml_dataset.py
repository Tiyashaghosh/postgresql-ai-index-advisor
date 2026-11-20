import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

INPUT_FILE = "data/generated/training_data.csv"
OUTPUT_FILE = "data/generated/ml_dataset.csv"


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def quote_identifier(name):
    """
    Safely quote PostgreSQL table/column identifiers.
    """
    return '"' + name.replace('"', '""') + '"'


def get_table_rows(table):
    """
    Get total number of rows in a table.
    """
    query = f"""
        SELECT COUNT(*)
        FROM {quote_identifier(table)}
    """

    cur.execute(query)
    return cur.fetchone()[0]


def get_column_cardinality(table, column):
    """
    Get number of distinct non-null values in a column.
    """
    query = f"""
        SELECT COUNT(DISTINCT {quote_identifier(column)})
        FROM {quote_identifier(table)}
    """

    cur.execute(query)
    return cur.fetchone()[0]


def get_data_type(table, column):
    """
    Get PostgreSQL data type of a column.
    """
    query = """
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = %s
          AND column_name = %s
    """

    cur.execute(query, (table, column))

    result = cur.fetchone()

    if result:
        return result[0]

    return "unknown"


def get_frequency(table, column, query_type, test_value):
    """
    Calculate the actual number of rows matched by the experiment.
    """

    table_q = quote_identifier(table)
    column_q = quote_identifier(column)

    # --------------------------------------------------------
    # EQUALITY
    # --------------------------------------------------------

    if query_type == "equality":

        query = f"""
            SELECT COUNT(*)
            FROM {table_q}
            WHERE {column_q} = %s
        """

        cur.execute(query, (test_value,))

        return cur.fetchone()[0]

    # --------------------------------------------------------
    # RANGE
    # --------------------------------------------------------

    elif query_type == "range":

        start_value, end_value = test_value.split(" -> ")

        query = f"""
            SELECT COUNT(*)
            FROM {table_q}
            WHERE {column_q} >= %s
              AND {column_q} < %s
        """

        cur.execute(
            query,
            (start_value, end_value)
        )

        return cur.fetchone()[0]

    # --------------------------------------------------------
    # IN
    # --------------------------------------------------------

    elif query_type == "in":

        values = [
            value.strip()
            for value in test_value.split(",")
        ]

        placeholders = ", ".join(
            ["%s"] * len(values)
        )

        query = f"""
            SELECT COUNT(*)
            FROM {table_q}
            WHERE {column_q} IN ({placeholders})
        """

        cur.execute(query, values)

        return cur.fetchone()[0]

    # --------------------------------------------------------
    # NOT NULL
    # --------------------------------------------------------

    elif query_type == "not_null":

        query = f"""
            SELECT COUNT(*)
            FROM {table_q}
            WHERE {column_q} IS NOT NULL
        """

        cur.execute(query)

        return cur.fetchone()[0]

    return None


# ============================================================
# LOAD TRAINING EXPERIMENT DATA
# ============================================================

print("=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")


# ============================================================
# CACHE DATABASE INFORMATION
# ============================================================

table_cache = {}
cardinality_cache = {}
datatype_cache = {}


def cached_table_rows(table):

    if table not in table_cache:
        table_cache[table] = get_table_rows(table)

    return table_cache[table]


def cached_cardinality(table, column):

    key = (table, column)

    if key not in cardinality_cache:
        cardinality_cache[key] = get_column_cardinality(
            table,
            column
        )

    return cardinality_cache[key]


def cached_datatype(table, column):

    key = (table, column)

    if key not in datatype_cache:
        datatype_cache[key] = get_data_type(
            table,
            column
        )

    return datatype_cache[key]


# ============================================================
# BUILD PRE-INDEX FEATURES
# ============================================================

print()
print("=" * 60)
print("BUILDING ML FEATURES")
print("=" * 60)

frequencies = []
table_rows_list = []
cardinality_list = []
datatype_list = []


for index, row in df.iterrows():

    table = row["table"]
    column = row["column"]
    query_type = row["query_type"]
    test_value = row["test_value"]

    # --------------------------------------------------------
    # Table size
    # --------------------------------------------------------

    table_rows = cached_table_rows(table)

    # --------------------------------------------------------
    # Column cardinality
    # --------------------------------------------------------

    cardinality = cached_cardinality(
        table,
        column
    )

    # --------------------------------------------------------
    # Data type
    # --------------------------------------------------------

    datatype = cached_datatype(
        table,
        column
    )

    # --------------------------------------------------------
    # Actual matching-row frequency
    # --------------------------------------------------------

    frequency = get_frequency(
        table,
        column,
        query_type,
        test_value
    )

    table_rows_list.append(table_rows)
    cardinality_list.append(cardinality)
    datatype_list.append(datatype)
    frequencies.append(frequency)

    if (index + 1) % 25 == 0:
        print(
            f"Processed {index + 1}/{len(df)} rows..."
        )


# ============================================================
# ADD COMPUTED FEATURES
# ============================================================

df["table_rows"] = table_rows_list

df["column_cardinality"] = cardinality_list

df["data_type"] = datatype_list

df["value_frequency"] = frequencies


# ------------------------------------------------------------
# Selectivity
# ------------------------------------------------------------

df["selectivity"] = (
    df["value_frequency"] /
    df["table_rows"]
)


# ------------------------------------------------------------
# Cardinality ratio
# ------------------------------------------------------------

df["cardinality_ratio"] = (
    df["column_cardinality"] /
    df["table_rows"]
)


# ============================================================
# HANDLE INVALID VALUES
# ============================================================

df["selectivity"] = (
    df["selectivity"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)

df["cardinality_ratio"] = (
    df["cardinality_ratio"]
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)


# ============================================================
# CATEGORICAL FEATURES
# ============================================================

categorical_columns = [
    "table",
    "column",
    "query_type",
    "data_type",
    "scan_before",
]


print()
print("Encoding categorical features...")

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    dtype=int
)


# ============================================================
# REMOVE INFORMATION THAT MUST NOT BE USED BY THE MODEL
# ============================================================

"""
IMPORTANT:

The model must only use information that is available BEFORE
creating the candidate index.

Therefore we remove:

1. test_value
   - The actual value used in the benchmark.
   - High-cardinality.
   - Can contain IDs, timestamps, etc.

2. execution_time_before
   - Deliberately excluded from the current model.

3. execution_time_after
   - Only known after creating the index.

4. cost_after
   - Only known after creating the index.

5. scan_after
   - Only known after creating the index.

6. improvement_percent
   - Directly derived from before/after performance.

7. absolute_improvement_ms
   - Directly derived from before/after performance.

8. index_recommended
   - This is the prediction target, not a feature.
"""

columns_to_remove = [
    "test_value",
    "execution_time_before",
    "execution_time_after",
    "cost_after",
    "scan_after",
    "improvement_percent",
    "absolute_improvement_ms",
]


df = df.drop(
    columns=columns_to_remove,
    errors="ignore"
)


# ============================================================
# TARGET
# ============================================================

target = "index_recommended"


if target not in df.columns:

    raise ValueError(
        "Target column 'index_recommended' "
        "was not found in training_data.csv"
    )


# ============================================================
# ENSURE ALL ML FEATURES ARE NUMERIC
# ============================================================

feature_columns = [
    column
    for column in df.columns
    if column != target
]


non_numeric_columns = df[
    feature_columns
].select_dtypes(
    exclude=["number", "bool"]
).columns.tolist()


if non_numeric_columns:

    print()
    print("ERROR: Non-numeric columns remain:")
    print(non_numeric_columns)

    raise ValueError(
        "ML dataset contains non-numeric features."
    )


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

# Put target at the end.

feature_columns = [
    column
    for column in df.columns
    if column != target
]

df = df[
    feature_columns + [target]
]


# ============================================================
# SAVE DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# CLOSE DATABASE
# ============================================================

cur.close()
conn.close()


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 60)
print("ML DATASET CREATED")
print("=" * 60)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print()
print("Class distribution:")

print(
    df[target].value_counts()
)


print()
print("Missing values:")

missing = df.isnull().sum()

missing = missing[
    missing > 0
]

print(missing)


print()
print("Non-numeric columns:")

print(
    df.select_dtypes(
        exclude=["number", "bool"]
    ).columns.tolist()
)


print()
print("Final feature columns:")

for column in feature_columns:
    print(f"  {column}")


print()
print("=" * 60)
print("DONE")
print("=" * 60)