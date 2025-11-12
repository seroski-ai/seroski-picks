from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import json

RAW_PATH = "/opt/airflow/data/raw_products.json"
BEST_PATH = "/opt/airflow/data/best_products.json"

def transform():
    with open(RAW_PATH, "r") as f:
        products = json.load(f)

    for p in products:
        p["id"] = f"raw-{p['id']}"
        p["title"] = p.pop("name")
        p["sentiment_score"] = round(0.2 + (p["rating"] / 5.0) * 0.8, 3)
        p["image_quality"] = round(min(1.0, p.get("images", 0) / 6.0), 3)
        p["final_score"] = round((p["rating"] * 0.4) + (p["sentiment_score"] * 0.4) + (p["image_quality"] * 0.2), 3)
        p["verdict"] = "✅ No major issues" if p["image_quality"] > 0.7 else "⚠ Possible build/image issues"

    best = sorted(products, key=lambda x: x["final_score"], reverse=True)[:3]

    with open(BEST_PATH, "w") as f:
        json.dump(best, f, indent=2)

    print("✅ Best JSON created")


def load_neon():
    with open(BEST_PATH, "r") as f:
        best = json.load(f)

    pg = PostgresHook(postgres_conn_id="neon_db")
    conn = pg.get_conn()
    cur = conn.cursor()

    # ✅ lower case column names to avoid case issues
    cur.execute("""
        CREATE TABLE IF NOT EXISTS best_products (
            id TEXT PRIMARY KEY,
            title TEXT,
            price INT,
            rating FLOAT,
            sentiment_score FLOAT,
            image_quality FLOAT,
            final_score FLOAT,
            verdict TEXT,
            createdat TIMESTAMP NOT NULL DEFAULT now(),
            updatedat TIMESTAMP NOT NULL DEFAULT now()
        );
    """)

    for p in best:
        cur.execute("""
            INSERT INTO best_products (
                id, title, price, rating, sentiment_score, image_quality, final_score, verdict, createdat, updatedat
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now(), now())
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                price = EXCLUDED.price,
                rating = EXCLUDED.rating,
                sentiment_score = EXCLUDED.sentiment_score,
                image_quality = EXCLUDED.image_quality,
                final_score = EXCLUDED.final_score,
                verdict = EXCLUDED.verdict,
                updatedat = now();
        """, (
            p["id"], p["title"], p["price"], p["rating"],
            p["sentiment_score"], p["image_quality"], p["final_score"], p["verdict"]
        ))

    conn.commit()
    cur.close()
    print("✅ Data pushed to Neon DB")


with DAG(
    "auto_json_to_neon_elt",
    start_date=datetime(2025, 1, 1),
    schedule="@once",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="raw_to_best", python_callable=transform)
    t2 = PythonOperator(task_id="best_to_neon", python_callable=load_neon)

    t1 >> t2  # 🔥 Auto chaining bro
