"""
FORMULA 1 Race Intelligence Platform
Epic 1 & 2: Data Extraction, Synthesis & Preparation

Generates comprehensive F1 race datasets covering 2010-2024 seasons,
including race results, driver standings, constructor performance,
lap times, pit stop strategy, circuit statistics, and qualifying sessions.
"""

import os, random, numpy as np, pandas as pd

np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

# ── Catalogs ──────────────────────────────────────────────────────────────────

SEASONS = list(range(2010, 2025))

CIRCUITS = [
    {"name": "Bahrain International Circuit",    "location": "Sakhir",         "country": "Bahrain",      "region": "Middle East",     "laps": 57, "length_km": 5.412, "type": "Street-like", "first_gp": 2004},
    {"name": "Saudi Arabian Street Circuit",     "location": "Jeddah",         "country": "Saudi Arabia", "region": "Middle East",     "laps": 50, "length_km": 6.174, "type": "Street",       "first_gp": 2021},
    {"name": "Albert Park Circuit",              "location": "Melbourne",       "country": "Australia",    "region": "Asia-Pacific",    "laps": 58, "length_km": 5.278, "type": "Street-like", "first_gp": 1996},
    {"name": "Suzuka International Racing Course","location": "Suzuka",         "country": "Japan",        "region": "Asia-Pacific",    "laps": 53, "length_km": 5.807, "type": "Permanent",    "first_gp": 1987},
    {"name": "Shanghai International Circuit",   "location": "Shanghai",        "country": "China",        "region": "Asia-Pacific",    "laps": 56, "length_km": 5.451, "type": "Permanent",    "first_gp": 2004},
    {"name": "Miami International Autodrome",    "location": "Miami",           "country": "USA",          "region": "Americas",        "laps": 57, "length_km": 5.412, "type": "Street",       "first_gp": 2022},
    {"name": "Circuit de Monaco",                "location": "Monte Carlo",     "country": "Monaco",       "region": "Europe",          "laps": 78, "length_km": 3.337, "type": "Street",       "first_gp": 1950},
    {"name": "Circuit de Catalunya",             "location": "Barcelona",       "country": "Spain",        "region": "Europe",          "laps": 66, "length_km": 4.657, "type": "Permanent",    "first_gp": 1991},
    {"name": "Circuit Gilles Villeneuve",        "location": "Montreal",        "country": "Canada",       "region": "Americas",        "laps": 70, "length_km": 4.361, "type": "Street-like", "first_gp": 1978},
    {"name": "Red Bull Ring",                    "location": "Spielberg",       "country": "Austria",      "region": "Europe",          "laps": 71, "length_km": 4.318, "type": "Permanent",    "first_gp": 1970},
    {"name": "Silverstone Circuit",              "location": "Silverstone",     "country": "UK",           "region": "Europe",          "laps": 52, "length_km": 5.891, "type": "Permanent",    "first_gp": 1950},
    {"name": "Hungaroring",                      "location": "Budapest",        "country": "Hungary",      "region": "Europe",          "laps": 70, "length_km": 4.381, "type": "Permanent",    "first_gp": 1986},
    {"name": "Circuit de Spa-Francorchamps",     "location": "Stavelot",        "country": "Belgium",      "region": "Europe",          "laps": 44, "length_km": 7.004, "type": "Permanent",    "first_gp": 1950},
    {"name": "Circuit Zandvoort",                "location": "Zandvoort",       "country": "Netherlands",  "region": "Europe",          "laps": 72, "length_km": 4.259, "type": "Permanent",    "first_gp": 1952},
    {"name": "Autodromo Nazionale Monza",        "location": "Monza",           "country": "Italy",        "region": "Europe",          "laps": 53, "length_km": 5.793, "type": "Permanent",    "first_gp": 1950},
    {"name": "Marina Bay Street Circuit",        "location": "Singapore",       "country": "Singapore",    "region": "Asia-Pacific",    "laps": 61, "length_km": 4.940, "type": "Street",       "first_gp": 2008},
    {"name": "Circuit of the Americas",          "location": "Austin",          "country": "USA",          "region": "Americas",        "laps": 56, "length_km": 5.513, "type": "Permanent",    "first_gp": 2012},
    {"name": "Autodromo Hermanos Rodriguez",     "location": "Mexico City",     "country": "Mexico",       "region": "Americas",        "laps": 71, "length_km": 4.304, "type": "Permanent",    "first_gp": 1963},
    {"name": "Autodromo Jose Carlos Pace",       "location": "Sao Paulo",       "country": "Brazil",       "region": "Americas",        "laps": 71, "length_km": 4.309, "type": "Permanent",    "first_gp": 1973},
    {"name": "Las Vegas Strip Circuit",          "location": "Las Vegas",       "country": "USA",          "region": "Americas",        "laps": 50, "length_km": 6.201, "type": "Street",       "first_gp": 2023},
    {"name": "Lusail International Circuit",     "location": "Lusail",          "country": "Qatar",        "region": "Middle East",     "laps": 57, "length_km": 5.380, "type": "Permanent",    "first_gp": 2021},
    {"name": "Yas Marina Circuit",               "location": "Abu Dhabi",       "country": "UAE",          "region": "Middle East",     "laps": 58, "length_km": 5.281, "type": "Permanent",    "first_gp": 2009},
]

DRIVERS = [
    # Current / Recent Champions & Top Drivers
    {"name": "Max Verstappen",      "nationality": "Dutch",       "team_era": {2022: "Red Bull Racing", 2023: "Red Bull Racing", 2024: "Red Bull Racing"}, "base_skill": 97, "active_from": 2015},
    {"name": "Lewis Hamilton",      "nationality": "British",     "team_era": {2010: "McLaren", 2013: "Mercedes", 2019: "Mercedes", 2024: "Mercedes"}, "base_skill": 98, "active_from": 2007},
    {"name": "Fernando Alonso",     "nationality": "Spanish",     "team_era": {2010: "Ferrari", 2013: "Ferrari", 2015: "McLaren", 2023: "Aston Martin"}, "base_skill": 96, "active_from": 2001},
    {"name": "Sebastian Vettel",    "nationality": "German",      "team_era": {2010: "Red Bull Racing", 2015: "Ferrari", 2021: "Aston Martin"}, "base_skill": 96, "active_from": 2007},
    {"name": "Charles Leclerc",     "nationality": "Monegasque",  "team_era": {2019: "Ferrari", 2024: "Ferrari"}, "base_skill": 93, "active_from": 2018},
    {"name": "Lando Norris",        "nationality": "British",     "team_era": {2019: "McLaren", 2024: "McLaren"}, "base_skill": 92, "active_from": 2019},
    {"name": "Carlos Sainz",        "nationality": "Spanish",     "team_era": {2015: "Toro Rosso", 2019: "McLaren", 2021: "Ferrari"}, "base_skill": 91, "active_from": 2015},
    {"name": "George Russell",      "nationality": "British",     "team_era": {2019: "Williams", 2022: "Mercedes"}, "base_skill": 91, "active_from": 2019},
    {"name": "Sergio Perez",        "nationality": "Mexican",     "team_era": {2011: "Force India", 2021: "Red Bull Racing"}, "base_skill": 89, "active_from": 2011},
    {"name": "Oscar Piastri",       "nationality": "Australian",  "team_era": {2023: "McLaren", 2024: "McLaren"}, "base_skill": 90, "active_from": 2023},
    {"name": "Lance Stroll",        "nationality": "Canadian",    "team_era": {2017: "Williams", 2019: "Racing Point", 2023: "Aston Martin"}, "base_skill": 82, "active_from": 2017},
    {"name": "Nico Hulkenberg",     "nationality": "German",      "team_era": {2010: "Williams", 2019: "Renault", 2023: "Haas"}, "base_skill": 86, "active_from": 2010},
    {"name": "Valtteri Bottas",     "nationality": "Finnish",     "team_era": {2013: "Williams", 2017: "Mercedes", 2022: "Alfa Romeo"}, "base_skill": 88, "active_from": 2013},
    {"name": "Daniel Ricciardo",    "nationality": "Australian",  "team_era": {2011: "HRT", 2014: "Red Bull Racing", 2019: "Renault", 2021: "McLaren", 2023: "RB"}, "base_skill": 90, "active_from": 2011},
    {"name": "Nico Rosberg",        "nationality": "German",      "team_era": {2010: "Mercedes", 2016: "Mercedes"}, "base_skill": 91, "active_from": 2006},
    {"name": "Kimi Raikkonen",      "nationality": "Finnish",     "team_era": {2010: "Lotus", 2014: "Ferrari", 2018: "Alfa Romeo"}, "base_skill": 92, "active_from": 2001},
    {"name": "Jenson Button",       "nationality": "British",     "team_era": {2010: "McLaren", 2014: "McLaren"}, "base_skill": 89, "active_from": 2000},
    {"name": "Esteban Ocon",        "nationality": "French",      "team_era": {2017: "Force India", 2020: "Renault", 2021: "Alpine"}, "base_skill": 85, "active_from": 2016},
    {"name": "Pierre Gasly",        "nationality": "French",      "team_era": {2017: "Toro Rosso", 2019: "Red Bull Racing", 2021: "AlphaTauri", 2023: "Alpine"}, "base_skill": 87, "active_from": 2017},
    {"name": "Yuki Tsunoda",        "nationality": "Japanese",    "team_era": {2021: "AlphaTauri", 2024: "RB"}, "base_skill": 83, "active_from": 2021},
]

CONSTRUCTORS = [
    {"name": "Red Bull Racing",  "nationality": "Austrian",    "power_unit": "Honda RBPT", "base_performance": 98},
    {"name": "Ferrari",          "nationality": "Italian",     "power_unit": "Ferrari",    "base_performance": 95},
    {"name": "Mercedes",         "nationality": "German",      "power_unit": "Mercedes",   "base_performance": 96},
    {"name": "McLaren",          "nationality": "British",     "power_unit": "Mercedes",   "base_performance": 92},
    {"name": "Aston Martin",     "nationality": "British",     "power_unit": "Mercedes",   "base_performance": 86},
    {"name": "Alpine",           "nationality": "French",      "power_unit": "Renault",    "base_performance": 82},
    {"name": "Williams",         "nationality": "British",     "power_unit": "Mercedes",   "base_performance": 78},
    {"name": "RB / AlphaTauri",  "nationality": "Italian",    "power_unit": "Honda RBPT", "base_performance": 80},
    {"name": "Haas F1 Team",     "nationality": "American",   "power_unit": "Ferrari",    "base_performance": 77},
    {"name": "Sauber / Alfa Romeo", "nationality": "Swiss",   "power_unit": "Ferrari",    "base_performance": 76},
]

TYRE_COMPOUNDS = ["Soft", "Medium", "Hard", "Intermediate", "Wet"]

SEASON_TEAMS = {
    yr: {
        "Max Verstappen": "Red Bull Racing", "Sergio Perez": "Red Bull Racing",
        "Lewis Hamilton": "Mercedes" if yr <= 2024 else "Ferrari",
        "George Russell": "Mercedes" if yr >= 2022 else "Williams",
        "Charles Leclerc": "Ferrari" if yr >= 2019 else "Sauber / Alfa Romeo",
        "Carlos Sainz": "Ferrari" if yr >= 2021 else ("McLaren" if yr >= 2019 else "Toro Rosso"),
        "Lando Norris": "McLaren" if yr >= 2019 else None,
        "Oscar Piastri": "McLaren" if yr >= 2023 else None,
        "Fernando Alonso": "Aston Martin" if yr >= 2023 else ("Alpine" if yr >= 2021 else ("McLaren" if yr >= 2015 else "Ferrari")),
        "Lance Stroll": "Aston Martin" if yr >= 2019 else "Williams",
        "Valtteri Bottas": "Alfa Romeo" if yr >= 2022 else ("Mercedes" if yr >= 2017 else "Williams"),
        "Esteban Ocon": "Alpine" if yr >= 2021 else "Renault",
        "Pierre Gasly": "Alpine" if yr >= 2023 else ("AlphaTauri" if yr >= 2020 else ("Red Bull Racing" if yr == 2019 else "AlphaTauri")),
        "Sebastian Vettel": "Aston Martin" if yr >= 2021 else ("Ferrari" if yr >= 2015 else "Red Bull Racing"),
        "Nico Rosberg": "Mercedes" if yr <= 2016 else None,
        "Kimi Raikkonen": "Alfa Romeo" if yr >= 2018 else ("Ferrari" if yr >= 2014 else "Lotus"),
        "Jenson Button": "McLaren" if yr <= 2014 else None,
        "Daniel Ricciardo": "RB / AlphaTauri" if yr == 2023 else ("McLaren" if yr >= 2021 else ("Renault" if yr >= 2019 else "Red Bull Racing")),
        "Nico Hulkenberg": "Haas F1 Team" if yr >= 2023 else ("Renault" if yr >= 2017 else "Force India"),
        "Yuki Tsunoda": "RB / AlphaTauri" if yr >= 2021 else None,
    }
    for yr in SEASONS
}

def get_team(driver_name, year):
    return SEASON_TEAMS.get(year, {}).get(driver_name)

def get_team_perf(team_name, year):
    base = {"Red Bull Racing": 98 if year >= 2022 else 90,
            "Mercedes": 96 if 2014 <= year <= 2021 else (88 if year >= 2022 else 84),
            "Ferrari": 93 if year >= 2022 else 88,
            "McLaren": 92 if year >= 2024 else (82 if year >= 2023 else 78),
            "Aston Martin": 86 if year == 2023 else 78,
            "Alpine": 82, "Williams": 76, "RB / AlphaTauri": 80,
            "Haas F1 Team": 77, "Sauber / Alfa Romeo": 76,
            "Force India": 80, "Lotus": 82, "Toro Rosso": 78}.get(team_name, 75)
    return base

def format_time(total_seconds):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = total_seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:06.3f}"
    return f"{m}:{s:06.3f}"

def generate_race_results():
    records = []
    race_id = 1001

    for season in SEASONS:
        n_races = 17 if season <= 2013 else (19 if season <= 2018 else (21 if season <= 2020 else min(23, 10 + season - 2018)))
        season_circuits = random.sample(CIRCUITS, min(n_races, len(CIRCUITS)))

        for round_num, circuit in enumerate(season_circuits, 1):
            active_drivers = [(d["name"], d["base_skill"]) for d in DRIVERS
                              if d["active_from"] <= season and get_team(d["name"], season)]

            random.shuffle(active_drivers)

            for finish_pos, (driver_name, driver_skill) in enumerate(active_drivers[:20], 1):
                team = get_team(driver_name, season) or "Unknown"
                team_perf = get_team_perf(team, season)

                performance_score = driver_skill * 0.6 + team_perf * 0.4 + np.random.normal(0, 6)
                grid_position = max(1, min(20, 21 - int(performance_score / 5) + random.randint(-4, 4)))

                dnf_prob = 0.05 + (0.02 if team_perf < 80 else 0)
                is_dnf = random.random() < dnf_prob

                race_time_base = circuit["laps"] * (circuit["length_km"] / 0.055)
                race_time = race_time_base * (1.0 + (finish_pos - 1) * 0.002 + np.random.uniform(-0.01, 0.01))

                fastest_lap = (circuit["length_km"] / 0.055) * 60 * np.random.uniform(0.96, 1.04)
                points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 10
                pts = 0 if is_dnf else points[finish_pos - 1]

                pit_stops = random.randint(1, 3)
                compound = random.choice(TYRE_COMPOUNDS[:3])
                overtakes = max(0, int(abs(grid_position - finish_pos) + np.random.poisson(2)))

                records.append({
                    "Race_ID": f"F1-{race_id}",
                    "Season": season,
                    "Round": round_num,
                    "Race_Name": f"{circuit['country']} Grand Prix",
                    "Circuit": circuit["name"],
                    "Circuit_Location": circuit["location"],
                    "Country": circuit["country"],
                    "Region": circuit["region"],
                    "Circuit_Type": circuit["type"],
                    "Circuit_Length_km": circuit["length_km"],
                    "Total_Laps": circuit["laps"],
                    "Driver": driver_name,
                    "Constructor": team,
                    "Grid_Position": grid_position,
                    "Finish_Position": finish_pos if not is_dnf else None,
                    "Race_Status": "DNF" if is_dnf else "Finished",
                    "Points_Scored": pts,
                    "Race_Time_Formatted": format_time(race_time) if not is_dnf else "DNF",
                    "Race_Time_Seconds": round(race_time, 3) if not is_dnf else None,
                    "Fastest_Lap_Seconds": round(fastest_lap, 3),
                    "Fastest_Lap_Formatted": format_time(fastest_lap),
                    "Pit_Stops": pit_stops,
                    "Primary_Compound": compound,
                    "Overtakes_Made": overtakes,
                    "Driver_Nationality": next((d["nationality"] for d in DRIVERS if d["name"] == driver_name), "Unknown"),
                })
                race_id += 1

    return pd.DataFrame(records)

def generate_driver_standings(df):
    standings = df.groupby(["Season", "Driver", "Constructor"]).agg(
        Total_Points=("Points_Scored", "sum"),
        Races_Entered=("Race_ID", "count"),
        Wins=("Finish_Position", lambda x: (x == 1).sum()),
        Podiums=("Finish_Position", lambda x: (x <= 3).sum()),
        DNFs=("Race_Status", lambda x: (x == "DNF").sum()),
        Avg_Grid=("Grid_Position", "mean"),
        Avg_Finish=("Finish_Position", "mean"),
        Best_Finish=("Finish_Position", "min"),
        Total_Overtakes=("Overtakes_Made", "sum"),
        Avg_Fastest_Lap=("Fastest_Lap_Seconds", "mean"),
    ).reset_index()

    standings["Avg_Grid"] = standings["Avg_Grid"].round(2)
    standings["Avg_Finish"] = standings["Avg_Finish"].round(2)
    standings["Avg_Fastest_Lap"] = standings["Avg_Fastest_Lap"].round(3)

    standings["Championship_Rank"] = standings.groupby("Season")["Total_Points"].rank(ascending=False, method="min").astype(int)
    standings["Win_Rate_Pct"] = (standings["Wins"] / standings["Races_Entered"] * 100).round(1)
    standings["Podium_Rate_Pct"] = (standings["Podiums"] / standings["Races_Entered"] * 100).round(1)
    standings["DNF_Rate_Pct"] = (standings["DNFs"] / standings["Races_Entered"] * 100).round(1)
    standings["Grid_vs_Finish_Delta"] = (standings["Avg_Grid"] - standings["Avg_Finish"]).round(2)

    return standings.sort_values(["Season", "Championship_Rank"])

def generate_constructor_standings(df):
    return df.groupby(["Season", "Constructor"]).agg(
        Total_Points=("Points_Scored", "sum"),
        Total_Wins=("Finish_Position", lambda x: (x == 1).sum()),
        Total_Podiums=("Finish_Position", lambda x: (x <= 3).sum()),
        Total_DNFs=("Race_Status", lambda x: (x == "DNF").sum()),
        Drivers_Used=("Driver", "nunique"),
        Avg_Fastest_Lap_Seconds=("Fastest_Lap_Seconds", "mean"),
    ).reset_index().assign(
        Constructor_Championship_Rank=lambda df_: df_.groupby("Season")["Total_Points"].rank(ascending=False, method="min").astype(int),
        Avg_Fastest_Lap_Seconds=lambda df_: df_["Avg_Fastest_Lap_Seconds"].round(3)
    ).sort_values(["Season", "Constructor_Championship_Rank"])

def main():
    print("=" * 60)
    print("F1 Race Intelligence — Epic 1 & 2: Data Pipeline")
    print("=" * 60)

    df = generate_race_results()
    print(f"Generated {len(df)} race result records.")

    raw_path = os.path.join(RAW_DIR, "F1_Race_Results_Raw.csv")
    df.to_csv(raw_path, index=False)
    print(f"Raw data: {raw_path}")

    # Driver standings
    driver_std = generate_driver_standings(df)
    ds_path = os.path.join(PROC_DIR, "F1_Driver_Standings.csv")
    driver_std.to_csv(ds_path, index=False)
    print(f"Driver standings: {ds_path}")

    # Constructor standings
    con_std = generate_constructor_standings(df)
    cs_path = os.path.join(PROC_DIR, "F1_Constructor_Standings.csv")
    con_std.to_csv(cs_path, index=False)
    print(f"Constructor standings: {cs_path}")

    # Circuit analytics
    cir_df = df.groupby("Circuit").agg(
        Country=("Country", "first"),
        Circuit_Type=("Circuit_Type", "first"),
        Total_Races=("Round", "nunique"),
        Avg_Overtakes=("Overtakes_Made", "mean"),
        Avg_Pit_Stops=("Pit_Stops", "mean"),
        Avg_Fastest_Lap_Seconds=("Fastest_Lap_Seconds", "mean"),
    ).reset_index().round(2)
    cir_path = os.path.join(PROC_DIR, "F1_Circuit_Analytics.csv")
    cir_df.to_csv(cir_path, index=False)
    print(f"Circuit analytics: {cir_path}")

    print("\n--- Key Statistics ---")
    print(f"Total Seasons:     {df['Season'].nunique()} (2010-2024)")
    print(f"Total Races:       {df[['Season','Round','Race_Name']].drop_duplicates().shape[0]}")
    print(f"Total Drivers:     {df['Driver'].nunique()}")
    print(f"Total Constructors:{df['Constructor'].nunique()}")
    print(f"Total Circuits:    {df['Circuit'].nunique()}")
    top_scorer = driver_std.groupby("Driver")["Total_Points"].sum().idxmax()
    print(f"All-Time Top Scorer: {top_scorer}")
    print("=" * 60)

if __name__ == "__main__":
    main()
