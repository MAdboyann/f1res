import fastf1
from database import SessionLocal, RaceResult

def save_race(year, gp):

    print(f"Loading {gp} {year}...")

    session = fastf1.get_session(year, gp, "R")
    session.load()

    db = SessionLocal()

    for _, row in session.results.iterrows():

        result = RaceResult(
            year=year,
            race=gp,
            position=int(row["Position"]),
            driver=row["FullName"],
            team=row["TeamName"]
        )

        db.add(result)

    db.commit()
    db.close()

    print(f"Saved {gp} {year}")


# 👉 add multiple races
races = [
    (2023, "Bahrain"),
    (2023, "Saudi Arabia"),
    (2023, "Monaco"),
    (2023, "Monza"),
]

for year, gp in races:
    save_race(year, gp)
