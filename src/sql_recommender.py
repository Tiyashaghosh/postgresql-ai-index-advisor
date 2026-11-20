import os
import re
import joblib
import psycopg2
import pandas as pd
# import shap

from dotenv import load_dotenv
from sqlglot import parse_one, exp


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

MODEL_PATH = "models/index_recommender.pkl"

REPEATS = 5

IMPROVEMENT_THRESHOLD = 20.0
ABSOLUTE_IMPROVEMENT_THRESHOLD = 1.0


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# DATABASE
# ============================================================

def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# ============================================================
# SQL CLEANING
# ============================================================

def clean_sql(sql):

    return sql.strip().rstrip(";").strip()


# ============================================================
# SQL PARSER
# ============================================================

def analyze_sql(sql):

    sql = clean_sql(sql)

    tree = parse_one(
        sql,
        dialect="postgres"
    )

    table_exp = tree.find(exp.Table)

    if table_exp is None:
        raise ValueError(
            "Could not identify table."
        )

    table = table_exp.name

    where = tree.find(exp.Where)

    if where is None:
        raise ValueError(
            "Query must contain a WHERE condition."
        )

    condition = where.this

    column = None
    query_type = None
    test_value = None

    # --------------------------------------------------------
    # Equality
    # --------------------------------------------------------

    if isinstance(condition, exp.EQ):

        query_type = "equality"

        if isinstance(
            condition.left,
            exp.Column
        ):

            column = condition.left.name

        test_value = condition.right.sql(
            dialect="postgres"
        )

    # --------------------------------------------------------
    # IN
    # --------------------------------------------------------

    elif isinstance(condition, exp.In):

        query_type = "in"

        if isinstance(
            condition.this,
            exp.Column
        ):

            column = condition.this.name

        test_value = condition.sql(
            dialect="postgres"
        )

    # --------------------------------------------------------
    # BETWEEN
    # --------------------------------------------------------

    elif isinstance(condition, exp.Between):

        query_type = "range"

        if isinstance(
            condition.this,
            exp.Column
        ):

            column = condition.this.name

        test_value = condition.sql(
            dialect="postgres"
        )

    # --------------------------------------------------------
    # Greater / Less
    # --------------------------------------------------------

    elif isinstance(
        condition,
        (
            exp.GT,
            exp.GTE,
            exp.LT,
            exp.LTE
        )
    ):

        query_type = "range"

        if isinstance(
            condition.left,
            exp.Column
        ):

            column = condition.left.name

        test_value = condition.sql(
            dialect="postgres"
        )

    # --------------------------------------------------------
    # IS NOT NULL
    # --------------------------------------------------------

    elif isinstance(condition, exp.Not):

        inner = condition.this

        if isinstance(inner, exp.Is):

            query_type = "not_null"

            if isinstance(
                inner.this,
                exp.Column
            ):

                column = inner.this.name

            test_value = "IS NOT NULL"

    else:

        raise ValueError(
            "Unsupported WHERE condition."
        )

    if column is None:

        raise ValueError(
            "Could not identify column."
        )

    return {
        "table": table,
        "column": column,
        "query_type": query_type,
        "test_value": test_value
    }


# ============================================================
# DATABASE FEATURES
# ============================================================

def get_table_rows(
    conn,
    table
):

    query = f'''
        SELECT COUNT(*)
        FROM "{table}";
    '''

    with conn.cursor() as cur:

        cur.execute(query)

        return cur.fetchone()[0]


def get_column_cardinality(
    conn,
    table,
    column
):

    query = f'''
        SELECT COUNT(DISTINCT "{column}")
        FROM "{table}"
        WHERE "{column}" IS NOT NULL;
    '''

    with conn.cursor() as cur:

        cur.execute(query)

        return cur.fetchone()[0]


def get_column_type(
    conn,
    table,
    column
):

    query = """
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = %s
        AND column_name = %s;
    """

    with conn.cursor() as cur:

        cur.execute(
            query,
            (table, column)
        )

        result = cur.fetchone()

    if result is None:

        raise ValueError(
            f"Column '{column}' not found."
        )

    return result[0]


def get_value_frequency(
    conn,
    sql
):

    sql = clean_sql(sql)

    query = f"""
        SELECT COUNT(*)
        FROM (
            {sql}
        ) AS query_result;
    """

    with conn.cursor() as cur:

        cur.execute(query)

        return cur.fetchone()[0]


def get_cost_before(
    conn,
    sql
):

    sql = clean_sql(sql)

    query = f"""
        EXPLAIN (
            FORMAT JSON
        )
        {sql};
    """

    with conn.cursor() as cur:

        cur.execute(query)

        result = cur.fetchone()[0]

    return result[0]["Plan"]["Total Cost"]


# ============================================================
# CALCULATE FEATURES
# ============================================================

def calculate_features(
    conn,
    sql,
    table,
    column
):

    table_rows = get_table_rows(
        conn,
        table
    )

    column_cardinality = get_column_cardinality(
        conn,
        table,
        column
    )

    value_frequency = get_value_frequency(
        conn,
        sql
    )

    data_type = get_column_type(
        conn,
        table,
        column
    )

    if table_rows > 0:

        selectivity = (
            value_frequency /
            table_rows
        )

        cardinality_ratio = (
            column_cardinality /
            table_rows
        )

    else:

        selectivity = 0
        cardinality_ratio = 0

    cost_before = get_cost_before(
        conn,
        sql
    )

    return {

        "table_rows": table_rows,

        "column_cardinality":
            column_cardinality,

        "value_frequency":
            value_frequency,

        "selectivity":
            selectivity,

        "cardinality_ratio":
            cardinality_ratio,

        "cost_before":
            cost_before,

        "data_type":
            data_type
    }


# ============================================================
# BUILD MODEL INPUT
# ============================================================

def build_model_input(
    features,
    table,
    column,
    query_type
):

    feature_names = model.feature_names_in_

    data = {
        feature: 0
        for feature in feature_names
    }

    data["table_rows"] = (
        features["table_rows"]
    )

    data["column_cardinality"] = (
        features["column_cardinality"]
    )

    data["value_frequency"] = (
        features["value_frequency"]
    )

    data["selectivity"] = (
        features["selectivity"]
    )

    data["cost_before"] = (
        features["cost_before"]
    )

    data["cardinality_ratio"] = (
        features["cardinality_ratio"]
    )

    table_feature = f"table_{table}"

    if table_feature in data:

        data[table_feature] = 1

    column_feature = f"column_{column}"

    if column_feature in data:

        data[column_feature] = 1

    query_feature = (
        f"query_type_{query_type}"
    )

    if query_feature in data:

        data[query_feature] = 1

    dtype_feature = (
        f"data_type_{features['data_type']}"
    )

    if dtype_feature in data:

        data[dtype_feature] = 1

    if "scan_before_Seq Scan" in data:

        data["scan_before_Seq Scan"] = 1

    return pd.DataFrame(
        [data],
        columns=feature_names
    )


# ============================================================
# SHAP EXPLANATION
# ============================================================

def get_shap_explanation(
    X
):
    try:
        import shap

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

    except ImportError:
        shap_values = None

    shap_values = explainer.shap_values(
        X
    )

    if isinstance(
        shap_values,
        list
    ):

        values = shap_values[1][0]

    else:

        if len(shap_values.shape) == 3:

            values = shap_values[
                0,
                :,
                1
            ]

        else:

            values = shap_values[0]

    explanation = pd.DataFrame({

        "feature": X.columns,

        "value": X.iloc[0].values,

        "shap_value": values

    })

    explanation[
        "absolute_shap"
    ] = explanation[
        "shap_value"
    ].abs()

    explanation = explanation.sort_values(
        "absolute_shap",
        ascending=False
    )

    return explanation


# ============================================================
# EXPLAINABLE FEATURES
# ============================================================

def display_shap_explanation(
    explanation
):

    print()
    print("=" * 60)
    print("WHY DID THE MODEL MAKE THIS PREDICTION?")
    print("=" * 60)

    print()

    # Ignore one-hot categorical features
    # for the human-readable explanation.

    useful_features = [
        "selectivity",
        "value_frequency",
        "cost_before",
        "table_rows",
        "column_cardinality",
        "cardinality_ratio"
    ]

    filtered = explanation[
        explanation["feature"].isin(
            useful_features
        )
    ]

    for _, row in filtered.head(6).iterrows():

        if row["shap_value"] > 0:

            direction = "supports index"

        else:

            direction = "opposes index"

        print(
            f"{row['feature']:<25} "
            f"SHAP={row['shap_value']:+.5f} "
            f"({direction})"
        )


# ============================================================
# FIND SCAN TYPE
# ============================================================

def find_scan_type(
    plan
):

    node_type = plan.get(
        "Node Type",
        ""
    )

    scan_types = [
        "Seq Scan",
        "Index Scan",
        "Index Only Scan",
        "Bitmap Heap Scan",
        "Bitmap Index Scan"
    ]

    if node_type in scan_types:

        return node_type

    for child in plan.get(
        "Plans",
        []
    ):

        result = find_scan_type(
            child
        )

        if result != "Unknown":

            return result

    return "Unknown"


# ============================================================
# RUN EXPLAIN ANALYZE
# ============================================================

def run_explain_analyze(
    conn,
    sql
):

    sql = clean_sql(sql)

    query = f"""
        EXPLAIN (
            ANALYZE,
            BUFFERS,
            FORMAT JSON
        )
        {sql};
    """

    with conn.cursor() as cur:

        cur.execute(query)

        result = cur.fetchone()[0]

    plan = result[0]

    return {

        "execution_time":
            plan["Execution Time"],

        "cost":
            plan["Plan"]["Total Cost"],

        "scan":
            find_scan_type(
                plan["Plan"]
            )
    }


# ============================================================
# BENCHMARK
# ============================================================

def benchmark_query(
    conn,
    sql
):

    results = []

    for _ in range(REPEATS):

        results.append(
            run_explain_analyze(
                conn,
                sql
            )
        )

    times = sorted(
        r["execution_time"]
        for r in results
    )

    middle = len(times) // 2

    if len(times) % 2 == 1:

        median_time = times[middle]

    else:

        median_time = (
            times[middle - 1]
            + times[middle]
        ) / 2

    closest = min(
        results,
        key=lambda r:
        abs(
            r["execution_time"]
            - median_time
        )
    )

    return {

        "execution_time":
            median_time,

        "cost":
            closest["cost"],

        "scan":
            closest["scan"]
    }


# ============================================================
# INDEX NAME
# ============================================================

def get_index_name(
    table,
    column
):

    if not re.match(
        r"^[A-Za-z_][A-Za-z0-9_]*$",
        table
    ):

        raise ValueError(
            "Invalid table name."
        )

    if not re.match(
        r"^[A-Za-z_][A-Za-z0-9_]*$",
        column
    ):

        raise ValueError(
            "Invalid column name."
        )

    return (
        f"idx_ml_{table}_{column}"
    )


# ============================================================
# CREATE INDEX
# ============================================================

def create_index(
    conn,
    table,
    column
):

    index_name = get_index_name(
        table,
        column
    )

    query = f'''
        CREATE INDEX "{index_name}"
        ON "{table}"("{column}");
    '''

    with conn.cursor() as cur:

        cur.execute(query)

    conn.commit()

    return index_name


# ============================================================
# DROP INDEX
# ============================================================

def drop_index(
    conn,
    index_name
):

    query = f'''
        DROP INDEX IF EXISTS "{index_name}";
    '''

    with conn.cursor() as cur:

        cur.execute(query)

    conn.commit()


# ============================================================
# VERIFY INDEX
# ============================================================

def verify_index(
    conn,
    sql,
    table,
    column
):

    print()
    print("=" * 60)
    print("POSTGRESQL VERIFICATION")
    print("=" * 60)

    print()
    print("Benchmarking WITHOUT index...")

    before = benchmark_query(
        conn,
        sql
    )

    print()
    print(
        f"Before execution time : "
        f"{before['execution_time']:.3f} ms"
    )

    print(
        f"Before cost           : "
        f"{before['cost']:.2f}"
    )

    print(
        f"Before scan           : "
        f"{before['scan']}"
    )

    print()
    print("Creating candidate index...")

    index_name = create_index(
        conn,
        table,
        column
    )

    try:

        with conn.cursor() as cur:

            cur.execute(
                f'ANALYZE "{table}";'
            )

        conn.commit()

        print(
            f"Created: {index_name}"
        )

        print()
        print("Benchmarking WITH index...")

        after = benchmark_query(
            conn,
            sql
        )

        print()
        print(
            f"After execution time  : "
            f"{after['execution_time']:.3f} ms"
        )

        print(
            f"After cost            : "
            f"{after['cost']:.2f}"
        )

        print(
            f"After scan            : "
            f"{after['scan']}"
        )

        absolute_improvement = (
            before["execution_time"]
            - after["execution_time"]
        )

        if before["execution_time"] > 0:

            improvement_percent = (
                absolute_improvement
                / before["execution_time"]
            ) * 100

        else:

            improvement_percent = 0

        verified = (
            improvement_percent
            >= IMPROVEMENT_THRESHOLD
            and
            absolute_improvement
            >= ABSOLUTE_IMPROVEMENT_THRESHOLD
        )

        return {

            "before": before,

            "after": after,

            "absolute_improvement":
                absolute_improvement,

            "improvement_percent":
                improvement_percent,

            "verified":
                verified
        }

    finally:

        print()
        print(
            "Removing temporary index..."
        )

        drop_index(
            conn,
            index_name
        )

        print(
            f"Removed: {index_name}"
        )


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def recommend_index(
    sql
):

    print()
    print("=" * 60)
    print("AI-ASSISTED SQL INDEX RECOMMENDER")
    print("=" * 60)

    print()
    print("SQL:")
    print(sql)

    # --------------------------------------------------------
    # Parse SQL
    # --------------------------------------------------------

    analysis = analyze_sql(sql)

    table = analysis["table"]
    column = analysis["column"]
    query_type = analysis["query_type"]

    print()
    print("Detected:")
    print(
        f"Table      : {table}"
    )
    print(
        f"Column     : {column}"
    )
    print(
        f"Query type : {query_type}"
    )

    # --------------------------------------------------------
    # Database connection
    # --------------------------------------------------------

    conn = get_connection()

    try:

        # ----------------------------------------------------
        # Feature extraction
        # ----------------------------------------------------

        features = calculate_features(
            conn,
            sql,
            table,
            column
        )

        print()
        print("=" * 60)
        print("FEATURES")
        print("=" * 60)

        print(
            f"Table rows        : "
            f"{features['table_rows']}"
        )

        print(
            f"Column cardinality: "
            f"{features['column_cardinality']}"
        )

        print(
            f"Value frequency   : "
            f"{features['value_frequency']}"
        )

        print(
            f"Selectivity       : "
            f"{features['selectivity']:.6f}"
        )

        print(
            f"Cardinality ratio : "
            f"{features['cardinality_ratio']:.6f}"
        )

        print(
            f"Query cost        : "
            f"{features['cost_before']:.2f}"
        )

        # ----------------------------------------------------
        # ML input
        # ----------------------------------------------------

        X = build_model_input(
            features,
            table,
            column,
            query_type
        )

        # ----------------------------------------------------
        # ML prediction
        # ----------------------------------------------------

        prediction = model.predict(
            X
        )[0]

        probability = model.predict_proba(
            X
        )[0][1]

        print()
        print("=" * 60)
        print("ML PREDICTION")
        print("=" * 60)

        print()
        print(
            f"Probability index is useful: "
            f"{probability:.2%}"
        )

        print(
            "Recommendation: "
            +
            (
                "INDEX LIKELY USEFUL"
                if prediction == 1
                else "INDEX NOT RECOMMENDED"
            )
        )

        # ----------------------------------------------------
        # SHAP
        # ----------------------------------------------------

        explanation = get_shap_explanation(
            X
        )

        display_shap_explanation(
            explanation
        )

        # ----------------------------------------------------
        # PostgreSQL verification
        # ----------------------------------------------------

        verification = verify_index(
            conn,
            sql,
            table,
            column
        )

    finally:

        conn.close()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print()

    print(
        f"ML prediction       : "
        f"{'USEFUL' if prediction == 1 else 'NOT USEFUL'}"
    )

    print(
        f"ML probability      : "
        f"{probability:.2%}"
    )

    print(
        f"Execution improvement: "
        f"{verification['improvement_percent']:.2f}%"
    )

    print(
        f"Absolute improvement: "
        f"{verification['absolute_improvement']:.3f} ms"
    )

    print(
        f"PostgreSQL verified : "
        f"{'YES' if verification['verified'] else 'NO'}"
    )

    print()

    if verification["verified"]:

        print(
            "FINAL RECOMMENDATION:"
        )

        print(
            f'CREATE INDEX '
            f'idx_{table}_{column} '
            f'ON "{table}"("{column}");'
        )

    else:

        print(
            "FINAL RECOMMENDATION:"
        )

        print(
            "Do NOT create the index "
            "based on the current verification."
        )

    print()

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sql = """
        SELECT *
        FROM orders
        WHERE customer_id = '9ef432eb6251297304e76186b10a928d';
    """

    recommend_index(sql)