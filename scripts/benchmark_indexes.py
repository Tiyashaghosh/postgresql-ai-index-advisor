import os
import re

import psycopg2
from dotenv import load_dotenv


load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()


query = """
SELECT *
FROM orders
WHERE customer_id = 'a973c08d3ed14b5f';
"""

index_name = "idx_orders_customer_id"


def get_execution_data(query):
    cursor.execute(
        "EXPLAIN (ANALYZE, FORMAT TEXT) " + query
    )

    result = "\n".join(row[0] for row in cursor.fetchall())

    # Extract execution time
    match = re.search(
        r"Execution Time: ([0-9.]+) ms",
        result
    )

    execution_time = float(match.group(1)) if match else None

    return result, execution_time


# ==========================================
# 1. REMOVE INDEX
# ==========================================

cursor.execute(
    f"DROP INDEX IF EXISTS {index_name};"
)

conn.commit()


# ==========================================
# 2. BEFORE INDEX
# ==========================================

before_plan, before_time = get_execution_data(query)

print("\n========== BEFORE INDEX ==========\n")
print(before_plan)

print(f"\nExecution time: {before_time} ms")


# ==========================================
# 3. CREATE INDEX
# ==========================================

cursor.execute("""
CREATE INDEX idx_orders_customer_id
ON orders(customer_id);
""")

conn.commit()


# ==========================================
# 4. AFTER INDEX
# ==========================================

after_plan, after_time = get_execution_data(query)

print("\n========== AFTER INDEX ==========\n")
print(after_plan)

print(f"\nExecution time: {after_time} ms")


# ==========================================
# 5. CALCULATE IMPROVEMENT
# ==========================================

if before_time and after_time:

    improvement = (
        (before_time - after_time)
        / before_time
    ) * 100

    print("\n========== RESULT ==========")

    print(f"Before:      {before_time:.3f} ms")
    print(f"After:       {after_time:.3f} ms")
    print(f"Improvement: {improvement:.2f}%")


cursor.close()
conn.close()