from flask import Flask, render_template, request, redirect
import psycopg2
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

# -----------------------------
# Load environment variables
# -----------------------------
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")

app = Flask(__name__)

# -----------------------------
# Database connection function
# -----------------------------
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

def init_db():
    """Create products table if it doesn't exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# -----------------------------
# Prometheus metrics
# -----------------------------
REQUEST_COUNT = Counter(
    "flask_app_requests_total", "Total requests to the Flask app"
)

CREATE_COUNT = Counter(
    "flask_app_creates_total", "Total number of products created"
)

UPDATE_COUNT = Counter(
    "flask_app_updates_total", "Total number of products updated"
)

DELETE_COUNT = Counter(
    "flask_app_deletes_total", "Total number of products deleted"
)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    REQUEST_COUNT.inc()  # count all requests
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", data=data)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    price = request.form["price"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    conn.commit()
    cur.close()
    conn.close()
    CREATE_COUNT.inc()  # count creation
    return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    id = request.form["id"]
    name = request.form["name"]
    price = request.form["price"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET name=%s, price=%s WHERE id=%s", (name, price, id))
    conn.commit()
    cur.close()
    conn.close()
    UPDATE_COUNT.inc()  # count update
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form["id"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    DELETE_COUNT.inc()  # count deletion
    return redirect("/")

# -----------------------------
# Prometheus metrics endpoint
# -----------------------------
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
