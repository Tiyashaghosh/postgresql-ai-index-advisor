import os
import joblib
import psycopg2
import pandas as pd
import shap

from dotenv import load_dotenv

from sql_recommender import (
    analyze_sql,
    calculate_features,
    build_model_input,
    get_connection
)


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

MODEL_PATH = "models/index_recommender.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# SHAP EXPLANATION
# ============================================================

def explain_prediction(
    sql
):

    print()
    print("=" * 60)
    print("SHAP MODEL EXPLANATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Connect to database
    # --------------------------------------------------------

    conn = get_connection()

    try:

        # ----------------------------------------------------
        # Analyze SQL
        # ----------------------------------------------------

        analysis = analyze_sql(sql)

        table = analysis["table"]
        column = analysis["column"]
        query_type = analysis["query_type"]

        # ----------------------------------------------------
        # Calculate features
        # ----------------------------------------------------

        features = calculate_features(
            conn,
            sql,
            table,
            column,
            query_type
        )

        # ----------------------------------------------------
        # Build exactly the same feature vector
        # used by the ML model
        # ----------------------------------------------------

        X = build_model_input(
            features,
            table,
            column,
            query_type
        )

    finally:

        conn.close()

    # ========================================================
    # MODEL PREDICTION
    # ========================================================

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1]

    print()
    print(
        f"Prediction: "
        f"{'INDEX USEFUL' if prediction == 1 else 'INDEX NOT USEFUL'}"
    )

    print(
        f"Probability: {probability:.2%}"
    )

    # ========================================================
    # SHAP EXPLAINER
    # ========================================================

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X)

    # --------------------------------------------------------
    # Handle SHAP output depending on SHAP version
    # --------------------------------------------------------

    if isinstance(shap_values, list):

        # Binary classifier:
        # class 1 = index useful

        shap_for_class_1 = shap_values[1][0]

    else:

        shap_array = shap_values

        if len(shap_array.shape) == 3:

            # Some SHAP versions return:
            # samples × features × classes

            shap_for_class_1 = shap_array[
                0,
                :,
                1
            ]

        else:

            shap_for_class_1 = shap_array[0]

    # ========================================================
    # CREATE EXPLANATION TABLE
    # ========================================================

    explanation = pd.DataFrame({

        "feature":
            X.columns,

        "value":
            X.iloc[0].values,

        "shap_value":
            shap_for_class_1

    })

    # --------------------------------------------------------
    # Absolute importance
    # --------------------------------------------------------

    explanation[
        "absolute_shap"
    ] = explanation[
        "shap_value"
    ].abs()

    explanation = explanation.sort_values(
        "absolute_shap",
        ascending=False
    )

    # ========================================================
    # DISPLAY TOP FEATURES
    # ========================================================

    print()
    print("=" * 60)
    print("TOP FEATURES INFLUENCING THE PREDICTION")
    print("=" * 60)

    print()

    for _, row in explanation.head(10).iterrows():

        feature = row["feature"]

        value = row["value"]

        shap_value = row["shap_value"]

        if shap_value > 0:

            direction = "SUPPORTS INDEX"

        else:

            direction = "OPPOSES INDEX"

        print(
            f"{feature:<40} "
            f"value={value:<12} "
            f"SHAP={shap_value:+.5f} "
            f"{direction}"
        )

    # ========================================================
    # SIMPLE HUMAN-READABLE EXPLANATION
    # ========================================================

    print()
    print("=" * 60)
    print("HUMAN-READABLE EXPLANATION")
    print("=" * 60)

    print()

    # --------------------------------------------------------
    # Important raw features
    # --------------------------------------------------------

    selectivity = features[
        "selectivity"
    ]

    frequency = features[
        "value_frequency"
    ]

    cardinality = features[
        "column_cardinality"
    ]

    table_rows = features[
        "table_rows"
    ]

    cost = features[
        "cost_before"
    ]

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    if prediction == 1:

        print(
            "The model recommends considering an index "
            "for this query."
        )

        print()

        print(
            f"• The query matches approximately "
            f"{frequency} row(s)."
        )

        print(
            f"• The table contains "
            f"{table_rows:,} rows."
        )

        print(
            f"• Query selectivity is "
            f"{selectivity:.6f}."
        )

        print(
            f"• The column has "
            f"{cardinality:,} distinct values."
        )

        print(
            f"• PostgreSQL's estimated query cost "
            f"is {cost:.2f}."
        )

        print()

        print(
            "These characteristics contributed to "
            "the model predicting that an index "
            "could be beneficial."
        )

    else:

        print(
            "The model does not recommend an index "
            "for this query."
        )

        print()

        print(
            f"• The query matches approximately "
            f"{frequency} row(s)."
        )

        print(
            f"• The table contains "
            f"{table_rows:,} rows."
        )

        print(
            f"• Query selectivity is "
            f"{selectivity:.6f}."
        )

        print(
            f"• The column has "
            f"{cardinality:,} distinct values."
        )

        print(
            f"• PostgreSQL's estimated query cost "
            f"is {cost:.2f}."
        )

        print()

        print(
            "These characteristics contributed to "
            "the model predicting that an index "
            "may not provide sufficient benefit."
        )

    return explanation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sql = """
        SELECT *
        FROM orders
        WHERE customer_id = '9ef432eb6251297304e76186b10a928d';
    """

    explain_prediction(sql)