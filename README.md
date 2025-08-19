# 🛠️ Simple CRUD App with Monitoring

This project is a **Flask + PostgreSQL CRUD application** with monitoring using **Prometheus** and **Grafana**.

## 📦 Pre-requisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

---

## 📁 Files and Purpose

| File                      | Purpose                                                             |
| ------------------------- | ------------------------------------------------------------------- |
| `app.py`                  | Flask application with CRUD endpoints and Prometheus metrics.       |
| `templates/index.html`    | HTML template for the CRUD UI.                                      |
| `docker-compose.yml`      | Defines services: Flask app, Postgres, Prometheus, Grafana.         |
| `Dockerfile`              | Builds the Flask app container image.                               |
| `requirements.txt`        | Python dependencies (Flask, psycopg2, prometheus-client, gunicorn). |
| `.env`                    | Environment variables (ports, DB credentials, etc.).                |
| `prometheus.yml`          | Prometheus configuration to scrape Flask app metrics.               |
| `crud-app-dashboard.json` | Exported Grafana dashboard for monitoring CRUD operations.          |

---

## ▶️ Running the Application

1. **Start services with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

2. **Verify containers**

   ```bash
   docker ps
   ```

3. **Access the application**

   * Flask App: [http://localhost:5000](http://localhost:5000)
   * Prometheus: [http://localhost:9090](http://localhost:9090)
   * Grafana: [http://localhost:3000](http://localhost:3000)

---

## 🧪 Testing the Application

* Visit **[http://localhost:5000](http://localhost:5000)** in your browser.
* Create, update, and delete products.
* Each action updates Prometheus metrics exposed at:
  [http://localhost:5000/metrics](http://localhost:5000/metrics)

---

## 📊 Setting up Grafana

### Add Data Source

1. Open Grafana → [http://localhost:3000](http://localhost:3000)
   Default login: `admin / admin`.
2. Go to **Connections → Data sources → Add data source**.
3. Select **Prometheus**.
4. Set **URL** to:

   ```
   http://prometheus:9090
   ```
5. Click **Save & Test**.

---

## 📈 Create Dashboard and Visualizations (Manual Way)

1. Go to **Dashboards → New → New Dashboard → Add Visualization**.
2. Choose the Prometheus data source.
3. Add panels with queries, for example:

   * **Requests per second**

     ```promql
     rate(flask_app_requests_total[1m])
     ```
   * **Products Created (5m)**

     ```promql
     increase(flask_app_creates_total[5m])
     ```
   * **Products Updated (per second)**

     ```promql
     rate(flask_app_updates_total[1m])
     ```
   * **Products Deleted (10m)**

     ```promql
     increase(flask_app_deletes_total[10m])
     ```
4. Give each panel a **Title** (e.g., *Total Requests*, *Products Created*).
5. Save the dashboard with a name like **CRUD Monitoring**.

---

## 📥 Import Dashboard (Alternative Way)

1. In Grafana, go to **Dashboards → New → Import**.
2. Click **Upload JSON file** and select `crud-app-dashboard.json`.
3. Choose your **Prometheus data source**.
4. Click **Import** → Dashboard loads automatically with all panels.

---

## 📸 Screenshots

### Grafana Dashboard

Here’s how the monitoring dashboard looks after setup:
<img width="1919" height="864" alt="Screenshot 2025-08-19 123656" src="https://github.com/user-attachments/assets/7c00e1f0-ba26-46e7-a625-71b7066dbacd" />

---

## 📝 Note from Me

I built this project as part of my **learning journey**.
It started simple — a Flask CRUD app — and step by step I added **Docker, PostgreSQL, Prometheus, and Grafana** to understand how real-world apps are monitored.

If you are just starting out like me, I hope this project helps you **learn bigger things by starting small**. 🚀
