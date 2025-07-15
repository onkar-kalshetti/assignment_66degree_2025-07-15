import pandas as pd
import sqlite3
import hashlib
import os

# ---------- Setup ----------
INPUT_FILE = "data/supermarket_sales.csv"
OUTPUT_DB = "output/supermarket_sales.db"
os.makedirs("output", exist_ok=True)

#Load and normalize CSV ----------
df = pd.read_csv(INPUT_FILE)

# Convert all column names to snake_case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# surrogate key generator ----------
def gen_id(*vals):
    return hashlib.md5("".join(map(str, vals)).encode()).hexdigest()

# Create dimension tables ----------
dim_customer = (
    df[["gender", "customer_type"]]
    .drop_duplicates()
    .assign(customer_id=lambda d: d.apply(lambda r: gen_id(r["gender"], r["customer_type"]), axis=1))
)

dim_product = (
    df[["product_line", "unit_price"]]
    .drop_duplicates()
    .assign(product_id=lambda d: d.apply(lambda r: gen_id(r["product_line"], r["unit_price"]), axis=1))
)

#  Enrich stage_sales with surrogate keys ----------
df_stage = df.merge(dim_customer, on=["gender", "customer_type"], how="left")
df_stage = df_stage.merge(dim_product, on=["product_line", "unit_price"], how="left")

# Write all to SQLite ----------
with sqlite3.connect(OUTPUT_DB) as conn:
    df_stage.to_sql("stage_sales", conn, if_exists="replace", index=False)
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)

print("stage_sales, dim_customer, dim_product created successfully")
