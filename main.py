import fastf1
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "F1 Explorer API running"}

@app.get("/race/{year}/{gp}")
def race_results(year: int, gp: str):

    session = fastf1.get_session(year, gp, "R")
    session.load()

    results = session.results

    data = []
    for _, row in results.iterrows():
        data.append({
            "position": int(row["Position"]),
            "driver": row["FullName"],
            "team": row["TeamName"]
        })

    return {
        "year": year,
        "race": gp,
        "results": data
    }
from functools import lru_cache
import fastf1

@lru_cache(maxsize=10)
def load_session(year, gp):
    session = fastf1.get_session(year, gp, "R")
    session.load()
    return session

@app.get("/race/{year}/{gp}")
def race_results(year: int, gp: str):

    session = load_session(year, gp)

    results = session.results

    data = []
    for _, row in results.iterrows():
        data.append({
            "position": int(row["Position"]),
            "driver": row["FullName"],
            "team": row["TeamName"]
        })

    return {
        "year": year,
        "race": gp,
        "results": data
    }
@app.get("/driver/{name}")
def driver(name: str):
    return {
        "driver": name,
        "note": "Next step: we will calculate real stats from all races"
    }
@app.get("/explain/compare/{d1}/{d2}")
def explain_compare(d1: str, d2: str):

    db = SessionLocal()

    p1 = find_driver(db, d1)
    p2 = find_driver(db, d2)

    def wins(r): return len([x for x in r if x.position == 1])
    def podiums(r): return len([x for x in r if x.position <= 3])

    return {
        "summary": f"{d1} vs {d2}",
        "analysis": [
            f"{d1} has {wins(p1)} wins and {podiums(p1)} podiums",
            f"{d2} has {wins(p2)} wins and {podiums(p2)} podiums"
        ]
    }
from database import SessionLocal, RaceResult
def find_driver(db, name: str):
    return db.query(RaceResult).filter(
        RaceResult.driver.ilike(f"%{name}%")
    ).all()
@app.get("/teams/{year}")
def team_stats(year: int):

    db = SessionLocal()

    results = db.query(RaceResult).filter_by(year=year).all()

    teams = {}

    for r in results:
        if r.team not in teams:
            teams[r.team] = {"wins": 0, "podiums": 0, "points": 0}

        if r.position == 1:
            teams[r.team]["wins"] += 1

        if r.position <= 3:
            teams[r.team]["podiums"] += 1

        points_table = {1:25,2:18,3:15,4:12,5:10,6:8,7:6,8:4,9:2,10:1}
        teams[r.team]["points"] += points_table.get(r.position, 0)

    sorted_teams = dict(
        sorted(teams.items(), key=lambda x: x[1]["points"], reverse=True)
    )

    return {
        "year": year,
        "dominance": sorted_teams,
        "summary": f"{list(sorted_teams.keys())[0]} is leading the season"
    }
