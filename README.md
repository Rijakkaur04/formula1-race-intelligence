# F1 Race Intelligence 🏁

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-purple)](https://formula1-race-intelligence.onrender.com)

## 🏎️ Project Overview

**F1 Race Intelligence** is a full-stack data analytics web application delivering deep insights into 15 seasons (2010–2024) of Formula 1 race data. Built for SmartBridge/SmartInternz Data Analytics internship program.

### 🔗 Live Links
- **GitHub Repository:** https://github.com/sanskritigangrade2007/FORMULA-1-Race-Intelligence-
- **Live Demo:** *(Will be updated after Render deployment)*

---

## 📊 Dataset Overview

| Metric | Value |
|--------|-------|
| Total Records | 3,424 race results |
| Seasons Covered | 2010–2024 (15 seasons) |
| Drivers Analysed | 20 elite drivers |
| Race Circuits | 22 global circuits |
| Constructors | 16 teams |
| Total Races | 263 Grand Prix events |

---

## 🖥️ Dashboard Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | KPI overview, trajectory charts |
| Drivers | `/drivers` | Championship standings & stats |
| Constructors | `/constructors` | Team performance battle |
| Circuits | `/circuits` | Circuit analytics & overtake data |
| Strategy | `/strategy` | Tyre compound & race narrative |
| Data Explorer | `/records` | Interactive searchable race data |
| Performance | `/performance` | Benchmark test results |

---

## ⚡ Performance Testing Results

| Test | Result | SLA |
|------|--------|-----|
| Data Ingestion | 4.65 ms | < 10 ms ✅ |
| Filter Query | 2.3 ms | < 5 ms ✅ |
| API Response | 8.1 ms | < 50 ms ✅ |
| Data Completeness | 100% | > 95% ✅ |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Flask 3.1.3
- **Data Processing:** Pandas 3.1.0, NumPy 2.4.4
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js 4.4
- **Deployment:** Render.com (free tier), Gunicorn WSGI
- **Database:** CSV-based analytical store (star schema design)

---

## 🚀 Local Setup

```bash
git clone https://github.com/sanskritigangrade2007/FORMULA-1-Race-Intelligence-.git
cd FORMULA-1-Race-Intelligence-
pip install -r requirements.txt
python wsgi.py
# Open: http://localhost:5000
```

---

## 📁 Project Structure

```
formula1_race_intelligence/
├── data/
│   ├── raw/F1_Race_Results_Raw.csv          # 3,424 records
│   └── processed/
│       ├── F1_Driver_Standings.csv
│       ├── F1_Constructor_Standings.csv
│       └── F1_Circuit_Analytics.csv
├── web_app/
│   ├── app.py                               # Flask app (15 routes)
│   ├── templates/                           # 7 HTML dashboards
│   └── static/                             # CSS + JS
├── scripts/data_pipeline.py                # Data generation pipeline
├── performance_testing/benchmark_tests.py
├── docs/Project_Report.md
├── wsgi.py                                  # Production WSGI entry
├── Procfile                                 # Render/Heroku config
├── render.yaml                              # Render blueprint
├── Dockerfile
└── requirements.txt
```

---

## 👩‍💻 Author

**Sanskriti Gangrade** — Data Analytics Intern, SmartBridge/SmartInternz  
GitHub: [@sanskritigangrade2007](https://github.com/sanskritigangrade2007)

---

*Project built as part of the SmartBridge Data Analytics with Tableau internship program.*
