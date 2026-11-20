import os
import random
import statistics
import time

import psycopg2
import pandas as pd
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

OUTPUT_FILE = "data/generated/training_data.csv"

# Keep 5 repetitions for reasonably stable measurements.
REPEATS = 5

# Index is considered useful only when BOTH conditions hold.
IMPROVEMENT_THRESHOLD = 20.0
ABSOLUTE_IMPROVEMENT_THRESHOLD = 1.0

RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ============================================================
# EXPERIMENT SIZE
# ============================================================

# Target roughly 500-700 genuine experiments.
#
# We generate:
#
# Equality  : many values from several columns
# Range     : many random date ranges
# IN        : different list sizes/combinations
# NOT NULL  : a smaller number because this is less realistic
#
# These are REAL PostgreSQL benchmarks, not synthetic SMOTE rows.

EQUALITY_SAMPLES_PER_COLUMN = 25

RANGE_SAMPLES_PER_RANGE_SIZE = 10

IN_SAMPLES_PER_COLUMN = 25

NOT_NULL_REPEATS = 3


# ============================================================
# CANDIDATE COLUMNS
# ============================================================

EQUALITY_COLUMNS = [
    ("orders", "customer_id"),
    ("orders", "order_status"),
    ("order_items", "product_id"),
    ("order_items", "seller_id"),
    ("products", "product_category_name"),
    ("customers", "customer_state"),
    ("sellers", "seller_state"),
]


RANGE_COLUMNS = [
    ("orders", "order_purchase_timestamp"),
    ("orders", "order_delivered_customer_date"),
]


IN_COLUMNS = [
    ("customers", "customer_state"),
    ("sellers", "seller_state"),
    ("orders", "order_status"),
    ("products", "product_category_name"),
]


NOT_NULL_COLUMNS = [
    ("orders", "customer_id"),
    ("orders", "order_status"),
    ("order_items", "product_id"),
    ("order_items", "seller_id"),
    ("customers", "customer_state"),
    ("sellers", "seller_state"),
    ("products", "product_category_name"),
]


# Date range sizes in days.
RANGE_SIZES = [
    1,
    3,
    7,
    14,
    30,
    60,
    90,
    120,
    180,
    270,
    365,
    500,
    700,
]


# ============================================================
# DATABASE
# ============================================================

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


# ============================================================
# HELPERS
# ============================================================

def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def get_distinct_values(table, column):
    """
    Get up to 1000 distinct non-null values.
    """

    query = f"""
        SELECT value
        FROM (
            SELECT DISTINCT {quote_identifier(column)} AS value
            FROM {quote_identifier(table)}
            WHERE {quote_identifier(column)} IS NOT NULL
        ) AS distinct_values
        ORDER BY RANDOM()
        LIMIT 1000;
    """

    cur.execute(query)

    return [row[0] for row in cur.fetchall()]


def get_min_max_timestamp(table, column):
    """
    Get minimum and maximum timestamp values.
    """

    query = f"""
        SELECT
            MIN({quote_identifier(column)}),
            MAX({quote_identifier(column)})
        FROM {quote_identifier(table)}
        WHERE {quote_identifier(column)} IS NOT NULL;
    """

    cur.execute(query)

    return cur.fetchone()


def get_execution_plan(query):
    """
    Execute EXPLAIN ANALYZE and return:
    execution time, total cost, scan type.
    """

    explain_query = f"""
        EXPLAIN (
            ANALYZE,
            BUFFERS,
            FORMAT JSON
        )
        {query}
    """

    cur.execute(explain_query)

    result = cur.fetchone()[0]

    plan = result[0]

    execution_time = plan["Execution Time"]

    total_cost = plan["Plan"]["Total Cost"]

    scan_type = find_scan_type(plan["Plan"])

    return (
        execution_time,
        total_cost,
        scan_type,
    )


def find_scan_type(plan):
    """
    Recursively find the main scan type.
    """

    node_type = plan.get("Node Type")

    if node_type:
        return node_type

    children = plan.get("Plans", [])

    for child in children:
        result = find_scan_type(child)

        if result:
            return result

    return "Unknown"


def benchmark_query(query):
    """
    Run the query multiple times and use the median execution time.

    Returns:
        median execution time
        cost
        scan type
    """

    times = []
    costs = []
    scans = []

    for _ in range(REPEATS):

        execution_time, cost, scan = get_execution_plan(query)

        times.append(execution_time)
        costs.append(cost)
        scans.append(scan)

    return (
        statistics.median(times),
        statistics.median(costs),
        scans[len(scans) // 2],
    )


def create_index(index_name, table, column):
    query = f"""
        CREATE INDEX {quote_identifier(index_name)}
        ON {quote_identifier(table)}
        ({quote_identifier(column)});
    """

    cur.execute(query)
    conn.commit()


def drop_index(index_name):

    query = f"""
        DROP INDEX IF EXISTS {quote_identifier(index_name)};
    """

    cur.execute(query)
    conn.commit()


def generate_index_name(table, column, experiment_id):

    safe_table = table.replace("-", "_")
    safe_column = column.replace("-", "_")

    return (
        f"tmp_idx_{safe_table}_{safe_column}_{experiment_id}"
    )


# ============================================================
# EXPERIMENT RUNNER
# ============================================================

results = []

experiment_id = 0


def run_experiment(
    table,
    column,
    query_type,
    test_value,
    query,
):
    global experiment_id

    experiment_id += 1

    index_name = generate_index_name(
        table,
        column,
        experiment_id
    )

    print(
        f"[{experiment_id}] "
        f"{table}.{column} | "
        f"{query_type}"
    )

    # --------------------------------------------------------
    # BEFORE INDEX
    # --------------------------------------------------------

    try:

        execution_before, cost_before, scan_before = (
            benchmark_query(query)
        )

    except Exception as e:

        print("  BEFORE failed:", e)

        conn.rollback()

        return

    # --------------------------------------------------------
    # CREATE INDEX
    # --------------------------------------------------------

    try:

        create_index(
            index_name,
            table,
            column
        )

        # Update PostgreSQL planner statistics.
        cur.execute(
            f"ANALYZE {quote_identifier(table)};"
        )

        conn.commit()

    except Exception as e:

        print("  INDEX CREATION failed:", e)

        conn.rollback()

        return

    # --------------------------------------------------------
    # AFTER INDEX
    # --------------------------------------------------------

    try:

        execution_after, cost_after, scan_after = (
            benchmark_query(query)
        )

    except Exception as e:

        print("  AFTER failed:", e)

        conn.rollback()

        try:
            drop_index(index_name)
        except Exception:
            conn.rollback()

        return

    # --------------------------------------------------------
    # DROP INDEX
    # --------------------------------------------------------

    try:

        drop_index(index_name)

        cur.execute(
            f"ANALYZE {quote_identifier(table)};"
        )

        conn.commit()

    except Exception as e:

        print("  INDEX DROP failed:", e)

        conn.rollback()

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    if execution_before > 0:

        improvement = (
            (
                execution_before
                - execution_after
            )
            / execution_before
        ) * 100

    else:

        improvement = 0.0

    absolute_improvement = (
        execution_before
        - execution_after
    )

    label = int(
        improvement >= IMPROVEMENT_THRESHOLD
        and
        absolute_improvement >=
        ABSOLUTE_IMPROVEMENT_THRESHOLD
    )

    results.append({
        "table": table,
        "column": column,
        "query_type": query_type,
        "test_value": str(test_value),

        "execution_time_before":
            execution_before,

        "execution_time_after":
            execution_after,

        "cost_before":
            cost_before,

        "cost_after":
            cost_after,

        "scan_before":
            scan_before,

        "scan_after":
            scan_after,

        "improvement_percent":
            improvement,

        "absolute_improvement_ms":
            absolute_improvement,

        "index_recommended":
            label,
    })


# ============================================================
# 1. EQUALITY EXPERIMENTS
# ============================================================

print()
print("=" * 60)
print("GENERATING EQUALITY EXPERIMENTS")
print("=" * 60)


for table, column in EQUALITY_COLUMNS:

    values = get_distinct_values(
        table,
        column
    )

    if not values:
        continue

    # Randomly sample more values than before.
    sample_size = min(
        EQUALITY_SAMPLES_PER_COLUMN,
        len(values)
    )

    selected_values = random.sample(
        values,
        sample_size
    )

    for value in selected_values:

        query = f"""
            SELECT *
            FROM {quote_identifier(table)}
            WHERE {quote_identifier(column)} = %s
        """

        # psycopg2 parameterized values cannot be directly used
        # inside EXPLAIN string, so safely convert the value.
        #
        # For text values we use SQL quoting.
        if isinstance(value, str):

            safe_value = value.replace(
                "'",
                "''"
            )

            query = f"""
                SELECT *
                FROM {quote_identifier(table)}
                WHERE {quote_identifier(column)}
                = '{safe_value}'
            """

        else:

            query = f"""
                SELECT *
                FROM {quote_identifier(table)}
                WHERE {quote_identifier(column)}
                = {value}
            """

        run_experiment(
            table,
            column,
            "equality",
            value,
            query
        )


# ============================================================
# 2. RANGE EXPERIMENTS
# ============================================================

print()
print("=" * 60)
print("GENERATING RANGE EXPERIMENTS")
print("=" * 60)


for table, column in RANGE_COLUMNS:

    min_date, max_date = get_min_max_timestamp(
        table,
        column
    )

    if min_date is None or max_date is None:
        continue

    total_days = (
        max_date - min_date
    ).days

    for range_size in RANGE_SIZES:

        if range_size >= total_days:
            continue

        for _ in range(
            RANGE_SAMPLES_PER_RANGE_SIZE
        ):

            max_start_offset = (
                total_days - range_size
            )

            start_offset = random.randint(
                0,
                max_start_offset
            )

            start_date = (
                min_date
                + pd.Timedelta(
                    days=start_offset
                )
            )

            end_date = (
                start_date
                + pd.Timedelta(
                    days=range_size
                )
            )

            start_string = start_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            end_string = end_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            query = f"""
                SELECT *
                FROM {quote_identifier(table)}
                WHERE {quote_identifier(column)}
                    >= '{start_string}'
                  AND {quote_identifier(column)}
                    < '{end_string}'
            """

            test_value = (
                f"{start_string} -> {end_string}"
            )

            run_experiment(
                table,
                column,
                "range",
                test_value,
                query
            )


# ============================================================
# 3. IN EXPERIMENTS
# ============================================================

print()
print("=" * 60)
print("GENERATING IN EXPERIMENTS")
print("=" * 60)


for table, column in IN_COLUMNS:

    values = get_distinct_values(
        table,
        column
    )

    if len(values) < 2:
        continue

    for _ in range(
        IN_SAMPLES_PER_COLUMN
    ):

        # Different IN list sizes.
        possible_sizes = [
            size
            for size in [1, 2, 3, 5, 10]
            if size <= len(values)
        ]

        list_size = random.choice(
            possible_sizes
        )

        selected_values = random.sample(
            values,
            list_size
        )

        sql_values = []

        for value in selected_values:

            if isinstance(value, str):

                safe_value = value.replace(
                    "'",
                    "''"
                )

                sql_values.append(
                    f"'{safe_value}'"
                )

            else:

                sql_values.append(
                    str(value)
                )

        query = f"""
            SELECT *
            FROM {quote_identifier(table)}
            WHERE {quote_identifier(column)}
            IN ({", ".join(sql_values)})
        """

        test_value = ",".join(
            str(value)
            for value in selected_values
        )

        run_experiment(
            table,
            column,
            "in",
            test_value,
            query
        )


# ============================================================
# 4. NOT NULL EXPERIMENTS
# ============================================================

print()
print("=" * 60)
print("GENERATING NOT NULL EXPERIMENTS")
print("=" * 60)


for table, column in NOT_NULL_COLUMNS:

    for _ in range(
        NOT_NULL_REPEATS
    ):

        query = f"""
            SELECT *
            FROM {quote_identifier(table)}
            WHERE {quote_identifier(column)}
            IS NOT NULL
        """

        run_experiment(
            table,
            column,
            "not_null",
            "IS NOT NULL",
            query
        )


# ============================================================
# SAVE DATA
# ============================================================

df = pd.DataFrame(results)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

before = len(df)

df = df.drop_duplicates(
    subset=[
        "table",
        "column",
        "query_type",
        "test_value",
    ]
)

after = len(df)


print()
print("=" * 60)
print("DATASET CLEANUP")
print("=" * 60)

print(f"Before: {before}")
print(f"After : {after}")
print(f"Removed: {before - after}")


# ============================================================
# SAVE
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 60)
print("TRAINING DATA GENERATED")
print("=" * 60)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print()
print("Class distribution:")

print(
    df["index_recommended"]
    .value_counts()
)


print()
print("By query type:")

print(
    pd.crosstab(
        df["query_type"],
        df["index_recommended"]
    )
)


print()
print("Saved to:")

print(OUTPUT_FILE)


# ============================================================
# CLOSE DATABASE
# ============================================================

cur.close()
conn.close()


print()
print("=" * 60)
print("DONE")
print("=" * 60)