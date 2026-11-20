import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sql_recommender import (
    analyze_sql,
    calculate_features,
    build_model_input,
    get_shap_explanation,
    verify_index,
    get_connection,
    model
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SQL Index Advisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* ================= HEADER ================= */

.hero {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1f2937 55%,
        #312e81 100%
    );

    padding: 1.7rem 2.2rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;

    box-shadow:
        0 8px 30px rgba(15, 23, 42, 0.12);
}

.hero-title {
    color: white;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
}


/* ================= SECTION TITLES ================= */

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #111827;
    margin-top: 1.6rem;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}


/* ================= CARDS ================= */

.info-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1rem 1.15rem;

    box-shadow:
        0 3px 12px rgba(15, 23, 42, 0.04);

    height: 100%;
}

.card-label {
    color: #64748b;
    font-size: 0.76rem;
    font-weight: 600;

    text-transform: uppercase;
    letter-spacing: 0.04em;

    margin-bottom: 0.3rem;
}

.card-value {
    color: #111827;
    font-size: 1.15rem;
    font-weight: 700;
}


/* ================= STATUS BOXES ================= */

.status-success {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;

    padding: 1rem 1.2rem;
    border-radius: 12px;

    font-weight: 600;
}

.status-warning {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;

    padding: 1rem 1.2rem;
    border-radius: 12px;

    font-weight: 600;
}

.status-danger {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;

    padding: 1rem 1.2rem;
    border-radius: 12px;

    font-weight: 600;
}


/* ================= RECOMMENDATION ================= */

.recommendation-card {
    background: linear-gradient(
        135deg,
        #ecfdf5,
        #f0fdf4
    );

    border: 1px solid #a7f3d0;

    border-radius: 16px;

    padding: 1.5rem;

    margin-top: 1rem;
}

.recommendation-title {
    color: #065f46;
    font-size: 1.3rem;
    font-weight: 700;

    margin-bottom: 0.5rem;
}

.recommendation-text {
    color: #334155;
    line-height: 1.6;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}


/* ================= BUTTON ================= */

.stButton > button {
    border-radius: 9px;
    font-weight: 600;
}


/* ================= DIVIDER ================= */

hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}


/* ================= HTML TABLES ================= */

.sql-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 14px;

    color: #111827 !important;
    background: white !important;

    border: 1px solid #e5e7eb;
    border-radius: 10px;
    overflow: hidden;
}

.sql-table th {
    background: #f1f5f9 !important;
    color: #111827 !important;

    padding: 10px 12px;

    text-align: left;
    font-weight: 700;

    border-bottom: 2px solid #cbd5e1;
}

.sql-table td {
    background: white !important;
    color: #111827 !important;

    padding: 10px 12px;

    border-bottom: 1px solid #e5e7eb;
}

.sql-table tr:last-child td {
    border-bottom: none;
}

.sql-table tr:hover td {
    background: #f8fafc !important;
}


/* ================= PLOTLY / SHAP TEXT ================= */

.js-plotly-plot {
    color: #111827;
}


/* ================= GENERAL TEXT ================= */

body {
    color: #111827;
}


/* ================= CODE BLOCK ================= */

pre {
    border-radius: 10px;
}


/* ================= TEXT AREA ================= */

textarea {
    border-radius: 10px !important;
}


/* ================= METRICS ================= */

[data-testid="stMetricValue"] {
    color: #111827 !important;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
}


/* ================= EXPANDERS ================= */

[data-testid="stExpander"] {
    border-radius: 10px;
}


/* ================= LINKS ================= */

a {
    color: #312e81;
}


/* ================= SCROLLBAR ================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# QUERY INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Analyze a Query</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Enter a PostgreSQL SELECT query with a supported filter condition.'
    '</div>',
    unsafe_allow_html=True
)


sql = st.text_area(
    "SQL Query",
    value="""SELECT *
FROM orders
WHERE customer_id = '9ef432eb6251297304e76186b10a928d';""",
    height=150,
    label_visibility="collapsed"
)


button_col1, button_col2, empty_col = st.columns(
    [1.1, 1.1, 5]
)

with button_col1:

    analyze_button = st.button(
        "⚡ Analyze Query",
        type="primary",
        use_container_width=True
    )

with button_col2:

    clear_button = st.button(
        "Clear",
        use_container_width=True
    )


if clear_button:
    st.rerun()

# ============================================================
# MAIN ANALYSIS
# ============================================================

if analyze_button:

    if not sql.strip():

        st.error("Please enter a SQL query.")

        st.stop()

    try:

        # ====================================================
        # STEP 1 — PARSE SQL
        # ====================================================

        with st.spinner("Analyzing SQL query..."):

            analysis = analyze_sql(sql)

        table = analysis["table"]
        column = analysis["column"]
        query_type = analysis["query_type"]


        # ====================================================
        # DATABASE CONNECTION
        # ====================================================

        conn = get_connection()

        try:

            # =================================================
            # STEP 2 — FEATURE EXTRACTION
            # =================================================

            with st.spinner(
                "Extracting PostgreSQL statistics..."
            ):

                features = calculate_features(
                    conn,
                    sql,
                    table,
                    column
                )


            # =================================================
            # STEP 3 — MODEL INPUT
            # =================================================

            X = build_model_input(
                features,
                table,
                column,
                query_type
            )


            # =================================================
            # STEP 4 — ML PREDICTION
            # =================================================

            prediction = model.predict(X)[0]

            probability = model.predict_proba(
                X
            )[0][1]


            # =================================================
            # STEP 5 — SHAP
            # =================================================

            explanation = get_shap_explanation(
                X
            )


            # =================================================
            # STEP 6 — POSTGRESQL VERIFICATION
            # =================================================

            with st.spinner(
                "Benchmarking query with PostgreSQL..."
            ):

                verification = verify_index(
                    conn,
                    sql,
                    table,
                    column
                )

        finally:

            conn.close()


        # ====================================================
        # QUERY PROFILE
        # ====================================================

        st.markdown(
            '<div class="section-title">Query Profile</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)


        cards = [

            (
                c1,
                "Table",
                table
            ),

            (
                c2,
                "Column",
                column
            ),

            (
                c3,
                "Query Type",
                query_type.upper()
            ),

            (
                c4,
                "Rows in Table",
                f"{features['table_rows']:,}"
            )
        ]


        for col, label, value in cards:

            with col:

                st.markdown(
                    f"""
<div class="info-card">

<div class="card-label">
{label}
</div>

<div class="card-value">
{value}
</div>

</div>
""",
                    unsafe_allow_html=True
                )


        # ====================================================
        # DATABASE STATISTICS
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'Database & Query Statistics'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Features supplied to the machine-learning model.'
            '</div>',
            unsafe_allow_html=True
        )


        f1, f2, f3, f4 = st.columns(4)


        feature_cards = [

            (
                f1,
                "Matching Rows",
                f"{features['value_frequency']:,}"
            ),

            (
                f2,
                "Selectivity",
                f"{features['selectivity']:.6f}"
            ),

            (
                f3,
                "Column Cardinality",
                f"{features['column_cardinality']:,}"
            ),

            (
                f4,
                "Query Cost",
                f"{features['cost_before']:.2f}"
            )
        ]


        for col, label, value in feature_cards:

            with col:

                st.markdown(
                    f"""
<div class="info-card">

<div class="card-label">
{label}
</div>

<div class="card-value">
{value}
</div>

</div>
""",
                    unsafe_allow_html=True
                )


        # ====================================================
        # ML RECOMMENDATION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'AI Recommendation'
            '</div>',
            unsafe_allow_html=True
        )


        ml_left, ml_right = st.columns(
            [1.5, 1]
        )


        with ml_left:

            if prediction == 1:

                st.markdown(
                    """
<div class="status-success">

✓ INDEX LIKELY USEFUL

<br><br>

The model predicts that an index on this
filter column is likely to improve query
performance.

</div>
""",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
<div class="status-warning">

⚠ INDEX MAY NOT BE BENEFICIAL

<br><br>

The model does not predict enough benefit
from creating this index.

</div>
""",
                    unsafe_allow_html=True
                )


        with ml_right:

            st.metric(
                "Index usefulness probability",
                f"{probability:.1%}"
            )


        # ====================================================
        # SHAP EXPLANATION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'Why did the model decide this?'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'SHAP shows how important features influenced '
            'the model prediction.'
            '</div>',
            unsafe_allow_html=True
        )


        useful_features = [

            "selectivity",

            "value_frequency",

            "cost_before",

            "table_rows",

            "column_cardinality",

            "cardinality_ratio"
        ]


        shap_display = explanation[
            explanation["feature"].isin(
                useful_features
            )
        ].copy()


        shap_display = shap_display[
            [
                "feature",
                "value",
                "shap_value"
            ]
        ]


        shap_display["Effect"] = (
            shap_display["shap_value"]
            .apply(
                lambda x:
                "Supports index"
                if x > 0
                else "Opposes index"
            )
        )


        shap_display = shap_display.sort_values(
            "shap_value",
            ascending=True
        )


        feature_names = {

            "selectivity":
                "Selectivity",

            "value_frequency":
                "Matching Rows",

            "cost_before":
                "Query Cost",

            "table_rows":
                "Table Rows",

            "column_cardinality":
                "Column Cardinality",

            "cardinality_ratio":
                "Cardinality Ratio"
        }


        shap_display["feature"] = (
            shap_display["feature"]
            .map(feature_names)
        )


        # ====================================================
        # SHAP CHART
        # ====================================================

        fig = go.Figure()


        for _, row in shap_display.iterrows():

            value = row["shap_value"]


            fig.add_trace(
                go.Bar(
                    x=[value],
                    y=[row["feature"]],
                    orientation="h",
                    text=[f"{value:+.4f}"],
                    textposition="outside",

                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "SHAP contribution: %{x:.4f}"
                        "<extra></extra>"
                    )
                )
            )


        fig.update_layout(

            height=350,

            showlegend=False,

            margin=dict(
                l=20,
                r=80,
                t=20,
                b=40
            ),

            xaxis_title="Contribution to prediction",

            yaxis_title="",

            plot_bgcolor="white",

            paper_bgcolor="white",

            font=dict(
                color="#334155"
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ====================================================
        # SHAP TABLE
        # ====================================================

        explanation_table = shap_display.copy()


        explanation_table["shap_value"] = (
            explanation_table["shap_value"]
            .map(
                lambda x: f"{x:+.4f}"
            )
        )


        explanation_table["value"] = (
            explanation_table["value"]
            .map(
                lambda x: f"{x:.6f}"
            )
        )


        explanation_table = (
            explanation_table.rename(
                columns={
                    "feature": "Feature",
                    "value": "Value",
                    "shap_value":
                        "SHAP Contribution",
                    "Effect": "Effect"
                }
            )
        )


        st.markdown(
    explanation_table.to_html(
        index=False,
        classes="sql-table",
        border=0
    ),
    unsafe_allow_html=True
)


        # ====================================================
        # POSTGRESQL VERIFICATION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'PostgreSQL Performance Verification'
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="section-subtitle">'
            'A temporary candidate index is created, the query '
            'is benchmarked, and the index is removed afterward.'
            '</div>',
            unsafe_allow_html=True
        )


        before = verification["before"]
        after = verification["after"]


        comparison = pd.DataFrame({

            "Metric": [

                "Execution Time",

                "Query Cost",

                "Scan Type"
            ],

            "Before Index": [

                f"{before['execution_time']:.3f} ms",

                f"{before['cost']:.2f}",

                before["scan"]
            ],

            "After Index": [

                f"{after['execution_time']:.3f} ms",

                f"{after['cost']:.2f}",

                after["scan"]
            ]
        })


        st.markdown(
            comparison.to_html(
                index=False,
                classes="sql-table",
                border=0
            ),
            unsafe_allow_html=True
        )


        # ====================================================
        # PERFORMANCE METRICS
        # ====================================================

        improvement = (
            verification["improvement_percent"]
        )

        absolute_improvement = (
            verification["absolute_improvement"]
        )


        m1, m2, m3 = st.columns(3)


        with m1:

            st.metric(
                "Execution Improvement",
                f"{improvement:.2f}%"
            )


        with m2:

            st.metric(
                "Time Saved",
                f"{absolute_improvement:.3f} ms"
            )


        with m3:

            if verification["verified"]:

                st.metric(
                    "Verification",
                    "PASSED"
                )

            else:

                st.metric(
                    "Verification",
                    "FAILED"
                )


        # ====================================================
        # FINAL RECOMMENDATION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            'Final Recommendation'
            '</div>',
            unsafe_allow_html=True
        )


        if verification["verified"]:

            st.markdown(
                """
<div class="recommendation-card">

<div class="recommendation-title">
✓ Index Verified as Beneficial
</div>

<div class="recommendation-text">

PostgreSQL confirmed that the candidate
index improved query performance enough
to satisfy the project's verification
criteria.

</div>

</div>
""",
                unsafe_allow_html=True
            )


            st.markdown(
                '<div class="section-subtitle">'
                'Recommended SQL'
                '</div>',
                unsafe_allow_html=True
            )


            index_sql = (
                f'CREATE INDEX idx_{table}_{column}\n'
                f'ON "{table}"("{column}");'
            )


            st.code(
                index_sql,
                language="sql"
            )


            st.caption(
                "✓ Candidate index was temporary and has already "
                "been removed from PostgreSQL."
            )


        else:

            st.markdown(
                """
<div class="status-warning">

⚠ Index recommendation was not verified.

The candidate index did not provide enough
measured improvement to satisfy the project's
verification threshold.

</div>
""",
                unsafe_allow_html=True
            )


        # ====================================================
        # TECHNICAL PIPELINE
        # ====================================================

        with st.expander(
            "View technical pipeline"
        ):

            st.markdown(
                """
**SQL Query**

↓

**SQLGlot Parser**

↓

**PostgreSQL Statistics**

↓

**Feature Engineering**

↓

**Random Forest Prediction**

↓

**SHAP Explanation**

↓

**Temporary Candidate Index**

↓

**EXPLAIN ANALYZE**

↓

**Before vs After Benchmark**

↓

**Final Recommendation**
"""
            )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        import traceback

        st.error(
            "The query could not be analyzed."
        )

        with st.expander(
            "Technical error details",
            expanded=True
        ):

            st.code(
                traceback.format_exc()
            )