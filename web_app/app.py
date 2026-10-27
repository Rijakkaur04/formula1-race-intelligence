"""
Formula 1 Race Intelligence - Flask Web Application
Full-stack analytics dashboard for F1 data (2010-2024)
"""

import os
import json
import pandas as pd
from flask import Flask, render_template, jsonify, send_file, request
from io import StringIO
import csv

app = Flask(__name__)

# ─── Data Loading ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")

def load_data():
    dfs = {}
    try:
        dfs["race_results"]   = pd.read_csv(os.path.join(RAW_DIR,  "F1_Race_Results_Raw.csv"))
        dfs["drivers"]        = pd.read_csv(os.path.join(DATA_DIR, "F1_Driver_Standings.csv"))
        dfs["constructors"]   = pd.read_csv(os.path.join(DATA_DIR, "F1_Constructor_Standings.csv"))
        dfs["circuits"]       = pd.read_csv(os.path.join(DATA_DIR, "F1_Circuit_Analytics.csv"))
    except Exception as e:
        print(f"Data load warning: {e}")
    return dfs

DATA = load_data()

def safe_int(v):
    try: return int(v)
    except: return 0

def safe_float(v):
    try: return round(float(v), 2)
    except: return 0.0

# ─── Page Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    df = DATA.get("race_results", pd.DataFrame())
    drivers_df = DATA.get("drivers", pd.DataFrame())
    constructors_df = DATA.get("constructors", pd.DataFrame())
    stats = {
        "total_races": safe_int(df["Race_Name"].nunique()) if not df.empty else 263,
        "total_drivers": safe_int(df["Driver"].nunique()) if not df.empty else 20,
        "total_circuits": safe_int(df["Circuit"].nunique()) if not df.empty else 22,
        "seasons": "2010–2024",
        "total_records": len(df),
        "champion_2024": "Max Verstappen",
        "constructor_2024": "Red Bull Racing",
    }
    top_drivers = []
    if not drivers_df.empty:
        top = drivers_df.sort_values("Total_Points", ascending=False).head(5)
        for _, r in top.iterrows():
            top_drivers.append({
                "name": r.get("Driver", ""),
                "points": safe_int(r.get("Total_Points", 0)),
                "wins": safe_int(r.get("Wins", 0)),
                "rank": safe_int(r.get("Championship_Rank", 0)),
            })
    return render_template("index.html", stats=stats, top_drivers=top_drivers)

@app.route("/drivers")
def drivers():
    drivers_df = DATA.get("drivers", pd.DataFrame())
    driver_list = []
    if not drivers_df.empty:
        for _, r in drivers_df.sort_values("Championship_Rank").iterrows():
            driver_list.append({
                "rank": safe_int(r.get("Championship_Rank", 0)),
                "driver": r.get("Driver", ""),
                "constructor": r.get("Constructor", ""),
                "points": safe_int(r.get("Total_Points", 0)),
                "wins": safe_int(r.get("Wins", 0)),
                "podiums": safe_int(r.get("Podiums", 0)),
                "dnfs": safe_int(r.get("DNFs", 0)),
                "win_rate": safe_float(r.get("Win_Rate_Pct", 0)),
            })
    return render_template("dashboard_drivers.html", drivers=driver_list)

@app.route("/constructors")
def constructors():
    constructors_df = DATA.get("constructors", pd.DataFrame())
    constructor_list = []
    if not constructors_df.empty:
        for _, r in constructors_df.sort_values("Constructor_Championship_Rank").iterrows():
            constructor_list.append({
                "rank": safe_int(r.get("Constructor_Championship_Rank", 0)),
                "constructor": r.get("Constructor", ""),
                "points": safe_int(r.get("Total_Points", 0)),
                "wins": safe_int(r.get("Total_Wins", 0)),
                "drivers": r.get("Top_Driver", ""),
            })
    return render_template("dashboard_constructors.html", constructors=constructor_list)

@app.route("/circuits")
def circuits():
    circuits_df = DATA.get("circuits", pd.DataFrame())
    circuit_list = []
    if not circuits_df.empty:
        for _, r in circuits_df.iterrows():
            circuit_list.append({
                "circuit": r.get("Circuit", ""),
                "races": safe_int(r.get("Total_Races", 0)),
                "avg_overtakes": safe_float(r.get("Avg_Overtakes", 0)),
                "dnf_rate": safe_float(r.get("DNF_Rate_Pct", 0)),
                "most_wins": r.get("Most_Wins_Driver", ""),
            })
    return render_template("dashboard_circuits.html", circuits=circuit_list)

@app.route("/strategy")
def strategy():
    return render_template("tableau_story.html")

@app.route("/records")
def records():
    df = DATA.get("race_results", pd.DataFrame())
    records_data = []
    if not df.empty:
        sample = df.head(200)
        for _, r in sample.iterrows():
            records_data.append({
                "season": safe_int(r.get("Season", 0)),
                "race": r.get("Race_Name", ""),
                "circuit": r.get("Circuit", ""),
                "driver": r.get("Driver", ""),
                "constructor": r.get("Constructor", ""),
                "grid": safe_int(r.get("Grid_Position", 0)),
                "finish": safe_int(r.get("Finish_Position", 0)),
                "points": safe_float(r.get("Points_Scored", 0)),
                "status": r.get("Race_Status", ""),
            })
    return render_template("data_explorer.html", records=records_data)

@app.route("/performance")
def performance():
    return render_template("performance.html")

# ─── API Routes ───────────────────────────────────────────────────────────────

@app.route("/api/stats")
def api_stats():
    df = DATA.get("race_results", pd.DataFrame())
    drivers_df = DATA.get("drivers", pd.DataFrame())
    constructors_df = DATA.get("constructors", pd.DataFrame())
    return jsonify({
        "total_races": safe_int(df["Race_Name"].nunique()) if not df.empty else 263,
        "total_records": len(df),
        "total_drivers": safe_int(df["Driver"].nunique()) if not df.empty else 20,
        "total_circuits": safe_int(df["Circuit"].nunique()) if not df.empty else 22,
        "total_constructors": safe_int(df["Constructor"].nunique()) if not df.empty else 16,
        "seasons": list(range(2010, 2025)),
        "champion_2024": "Max Verstappen",
    })

@app.route("/api/charts/driver-points")
def api_driver_points():
    drivers_df = DATA.get("drivers", pd.DataFrame())
    if drivers_df.empty:
        return jsonify({"labels": [], "data": []})
    top = drivers_df.sort_values("Total_Points", ascending=False).head(10)
    return jsonify({
        "labels": top["Driver"].tolist(),
        "data": top["Total_Points"].astype(int).tolist(),
        "wins": top["Wins"].astype(int).tolist(),
    })

@app.route("/api/charts/constructor-points")
def api_constructor_points():
    constructors_df = DATA.get("constructors", pd.DataFrame())
    if constructors_df.empty:
        return jsonify({"labels": [], "data": []})
    top = constructors_df.sort_values("Total_Points", ascending=False).head(10)
    return jsonify({
        "labels": top["Constructor"].tolist(),
        "data": top["Total_Points"].astype(int).tolist(),
        "wins": top["Total_Wins"].astype(int).tolist(),
    })

@app.route("/api/charts/circuit-analysis")
def api_circuit_analysis():
    circuits_df = DATA.get("circuits", pd.DataFrame())
    if circuits_df.empty:
        return jsonify({"labels": [], "overtakes": [], "dnf_rate": []})
    top = circuits_df.sort_values("Avg_Overtakes", ascending=False).head(12)
    return jsonify({
        "labels": top["Circuit"].tolist(),
        "overtakes": [safe_float(x) for x in top["Avg_Overtakes"].tolist()],
        "dnf_rate": [safe_float(x) for x in top["DNF_Rate_Pct"].tolist()],
    })

@app.route("/api/charts/season-trajectory")
def api_season_trajectory():
    df = DATA.get("race_results", pd.DataFrame())
    if df.empty:
        return jsonify({"seasons": [], "datasets": []})
    top5 = DATA.get("drivers", pd.DataFrame())
    if top5.empty:
        return jsonify({"seasons": [], "datasets": []})
    top5_names = top5.sort_values("Total_Points", ascending=False).head(5)["Driver"].tolist()
    seasons = sorted(df["Season"].unique().tolist())
    datasets = []
    colors = ["#e10600", "#00D2BE", "#FF8700", "#DC0000", "#0090FF"]
    for i, driver in enumerate(top5_names):
        pts_by_season = []
        ddf = df[df["Driver"] == driver]
        for s in seasons:
            pts = ddf[ddf["Season"] == s]["Points_Scored"].sum()
            pts_by_season.append(round(float(pts), 1))
        datasets.append({
            "label": driver,
            "data": pts_by_season,
            "borderColor": colors[i % len(colors)],
            "backgroundColor": colors[i % len(colors)] + "33",
        })
    return jsonify({"seasons": [str(s) for s in seasons], "datasets": datasets})

@app.route("/api/charts/tyre-strategy")
def api_tyre_strategy():
    df = DATA.get("race_results", pd.DataFrame())
    if df.empty or "Primary_Compound" not in df.columns:
        return jsonify({"labels": [], "data": []})
    compound_counts = df["Primary_Compound"].value_counts()
    return jsonify({
        "labels": compound_counts.index.tolist(),
        "data": compound_counts.values.tolist(),
    })

@app.route("/api/records")
def api_records():
    df = DATA.get("race_results", pd.DataFrame())
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    season = request.args.get("season", None)
    driver = request.args.get("driver", None)
    if df.empty:
        return jsonify({"data": [], "total": 0, "page": page})
    filtered = df.copy()
    if season:
        filtered = filtered[filtered["Season"] == int(season)]
    if driver:
        filtered = filtered[filtered["Driver"].str.contains(driver, case=False, na=False)]
    total = len(filtered)
    start = (page - 1) * per_page
    page_df = filtered.iloc[start:start + per_page]
    records = page_df.fillna("").to_dict(orient="records")
    return jsonify({"data": records, "total": total, "page": page, "per_page": per_page})

# ─── Download Routes ──────────────────────────────────────────────────────────

@app.route("/download/csv")
def download_csv():
    path = os.path.join(RAW_DIR, "F1_Race_Results_Raw.csv")
    return send_file(path, as_attachment=True, download_name="F1_Race_Results.csv")

@app.route("/download/driver-standings")
def download_driver_standings():
    path = os.path.join(DATA_DIR, "F1_Driver_Standings.csv")
    return send_file(path, as_attachment=True, download_name="F1_Driver_Standings.csv")

@app.route("/download/circuit-analytics")
def download_circuits():
    path = os.path.join(DATA_DIR, "F1_Circuit_Analytics.csv")
    return send_file(path, as_attachment=True, download_name="F1_Circuit_Analytics.csv")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "project": "F1 Race Intelligence", "version": "1.0.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
